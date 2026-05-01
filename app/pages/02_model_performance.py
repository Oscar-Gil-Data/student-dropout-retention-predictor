import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from sklearn.metrics import (
    classification_report, confusion_matrix,
    ConfusionMatrixDisplay, roc_curve, auc,
    f1_score, roc_auc_score
)
from sklearn.preprocessing import label_binarize
import joblib, json, os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.predict import load_meta, load_model

st.header("Model Performance")
st.caption("Evaluation on the held-out test set (20% of 4,424 students, stratified split).")

CLASS_COLORS = {'Dropout': '#378ADD', 'Enrolled': '#D85A30', 'Graduate': '#639922'}
CLASS_ORDER  = ['Dropout', 'Enrolled', 'Graduate']

# ── Load artifacts ────────────────────────────────────────────────────
meta   = load_meta()
classes = meta['classes']

BASE = os.path.join(os.path.dirname(__file__), '../..')
preds_path = os.path.join(BASE, 'data/processed/test_predictions.parquet')
preds = pd.read_parquet(preds_path)

lr = load_model('Logistic Regression')
rf = load_model('Random Forest')

X_test = pd.read_parquet(os.path.join(BASE, 'data/processed/X_test.parquet'))
y_test = pd.read_parquet(os.path.join(BASE, 'data/processed/y_test.parquet')).squeeze()

y_pred_lr = preds['y_pred_lr'].values
y_pred_rf = preds['y_pred_rf'].values
y_proba_lr = lr.predict_proba(X_test)
y_proba_rf = rf.predict_proba(X_test)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Confusion matrices",
    "Per-class F1",
    "ROC curves",
    "Feature importance",
    "McNemar's test"
])

# ── Tab 1: Confusion matrices ─────────────────────────────────────────
with tab1:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, y_pred, title in zip(
        axes,
        [y_pred_lr, y_pred_rf],
        ['Logistic Regression', 'Random Forest']
    ):
        cm = confusion_matrix(y_test, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
        disp.plot(ax=ax, colorbar=False, cmap='Blues')
        ax.set_title(title, fontweight='bold')
    plt.suptitle('Confusion matrices -- test set', fontsize=13, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)

# ── Tab 2: Per-class F1 ───────────────────────────────────────────────
with tab2:
    f1_lr = f1_score(y_test, y_pred_lr, average=None)
    f1_rf = f1_score(y_test, y_pred_rf, average=None)

    f1_df = pd.DataFrame({
        'Class':                CLASS_ORDER,
        'Logistic Regression':  f1_lr.round(3),
        'Random Forest':        f1_rf.round(3),
    })

    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(f1_df, use_container_width=True, hide_index=True)
        st.metric("LR macro F1",  f"{f1_score(y_test, y_pred_lr, average='macro'):.4f}")
        st.metric("RF macro F1",  f"{f1_score(y_test, y_pred_rf, average='macro'):.4f}")

    with col2:
        x = np.arange(len(classes))
        width = 0.35
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(x - width/2, f1_lr, width, label='Logistic Regression', color='#7F77DD', alpha=0.85)
        ax.bar(x + width/2, f1_rf, width, label='Random Forest',       color='#4A9B6F', alpha=0.85)
        ax.set_xticks(x)
        ax.set_xticklabels(classes)
        ax.set_ylabel('F1 Score')
        ax.set_ylim(0, 1)
        ax.set_title('Per-class F1 comparison', fontweight='bold')
        ax.legend(loc='lower right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)

# ── Tab 3: ROC curves ─────────────────────────────────────────────────
with tab3:
    y_test_bin = label_binarize(y_test, classes=[0, 1, 2])
    auc_lr = roc_auc_score(y_test_bin, y_proba_lr, multi_class='ovr', average='macro')
    auc_rf = roc_auc_score(y_test_bin, y_proba_rf, multi_class='ovr', average='macro')

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for i, cls in enumerate(classes):
        for model_name, y_proba, ls, color in [
            ('Logistic Regression', y_proba_lr, '--', '#7F77DD'),
            ('Random Forest',       y_proba_rf, '-',  '#4A9B6F'),
        ]:
            fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
            roc_auc = auc(fpr, tpr)
            axes[i].plot(fpr, tpr, linestyle=ls, color=color, linewidth=2,
                         label=f'{model_name} (AUC={roc_auc:.3f})')
        axes[i].plot([0, 1], [0, 1], 'k:', linewidth=1, alpha=0.5)
        axes[i].set_title(f'{cls} (one-vs-rest)', fontweight='bold')
        axes[i].set_xlabel('False positive rate')
        axes[i].set_ylabel('True positive rate')
        axes[i].legend(loc='lower right', fontsize=8)
        axes[i].set_xlim([0, 1])
        axes[i].set_ylim([0, 1.02])
        axes[i].spines['top'].set_visible(False)
        axes[i].spines['right'].set_visible(False)
    plt.suptitle(
        f'ROC curves -- LR macro AUC={auc_lr:.3f} | RF macro AUC={auc_rf:.3f}',
        fontsize=12, fontweight='bold'
    )
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)

# ── Tab 4: McNemar ────────────────────────────────────────────────────
with tab5:
    from statsmodels.stats.contingency_tables import mcnemar

    lr_correct = (preds['y_pred_lr'] == preds['y_test']).astype(int)
    rf_correct = (preds['y_pred_rf'] == preds['y_test']).astype(int)

    a = ((lr_correct == 1) & (rf_correct == 1)).sum()
    b = ((lr_correct == 1) & (rf_correct == 0)).sum()
    c = ((lr_correct == 0) & (rf_correct == 1)).sum()
    d = ((lr_correct == 0) & (rf_correct == 0)).sum()

    table = np.array([[a, b], [c, d]])
    res   = mcnemar(table, exact=False, correction=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### Contingency table")
        ct = pd.DataFrame(
            table,
            index=['LR correct', 'LR wrong'],
            columns=['RF correct', 'RF wrong']
        )
        st.dataframe(ct, use_container_width=True)
        st.caption(f"Disagreement cells (b={b}, c={c}) -- {b+c} of {len(preds)} total ({(b+c)/len(preds):.1%})")

    with col2:
        st.markdown("#### Test result")
        st.metric("Chi-square statistic", f"{res.statistic:.4f}")
        st.metric("p-value", f"{res.pvalue:.4f}")

        ALPHA = 0.05
        if res.pvalue < ALPHA:
            winner = 'Logistic Regression' if b > c else 'Random Forest'
            st.success(f"Significant at p<{ALPHA}. **{winner}** makes significantly fewer errors.")
        else:
            st.info(f"Not significant at p<{ALPHA}. Neither model is statistically superior.")

    st.divider()
    st.markdown("#### Per-class McNemar results")

    per_class = []
    for idx, cls in enumerate(classes):
        mask = preds['y_test'] == idx
        lr_c = lr_correct[mask]
        rf_c = rf_correct[mask]
        b_c  = ((lr_c == 1) & (rf_c == 0)).sum()
        c_c  = ((lr_c == 0) & (rf_c == 1)).sum()
        tbl  = np.array([[((lr_c==1)&(rf_c==1)).sum(), b_c],
                          [c_c, ((lr_c==0)&(rf_c==0)).sum()]])
        try:
            r = mcnemar(tbl, exact=(b_c+c_c)<=25, correction=(b_c+c_c)>25)
            pval = r.pvalue
        except Exception:
            pval = 1.0
        per_class.append({
            'Class': cls,
            'n': int(mask.sum()),
            'LR only correct (b)': int(b_c),
            'RF only correct (c)': int(c_c),
            'p-value': round(pval, 4),
            'Significant': pval < ALPHA,
            'Better model': ('LR' if b_c > c_c else 'RF') if pval < ALPHA else 'no sig. diff.'
        })

    st.dataframe(pd.DataFrame(per_class), use_container_width=True, hide_index=True)

    st.markdown("""
    **Interpretation:** RF is statistically superior overall (p=0.0042) and wins on Dropout
    and Graduate. LR is significantly better on the Enrolled class (p<0.0001) -- the minority
    class most relevant to early intervention. Model selection should be use-case driven.
    """)

# ── Tab 5: Feature importance ─────────────────────────────────────────
with tab4:
    st.markdown("#### Random Forest -- feature importance")
    st.caption("Mean decrease in impurity across all trees. Does not indicate direction.")

    importance_df = pd.DataFrame({
        'feature':    X_test.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=True).tail(15)

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(importance_df['feature'], importance_df['importance'], color='#4A9B6F', alpha=0.85)
    ax.set_xlabel('Mean decrease in impurity')
    ax.set_title('Random Forest -- top 15 feature importances', fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)

    st.divider()
    st.markdown("#### Logistic Regression -- coefficients per class")
    st.caption("Red = pushes toward that class. Blue = pushes away from that class.")

    coef_df = pd.DataFrame(
        lr.coef_,
        index=classes,
        columns=X_test.columns
    ).T

    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    for i, cls in enumerate(classes):
        top = coef_df[cls].abs().sort_values(ascending=True).tail(15)
        colors = ['#D85A30' if coef_df[cls][feat] > 0 else '#378ADD' for feat in top.index]
        axes[i].barh(top.index, coef_df[cls][top.index], color=colors)
        axes[i].axvline(x=0, color='black', linewidth=0.8)
        axes[i].set_title(f'{cls} coefficients', fontweight='bold')
        axes[i].set_xlabel('Coefficient value')
        axes[i].spines['top'].set_visible(False)
        axes[i].spines['right'].set_visible(False)

    plt.suptitle(
        'Logistic Regression -- top 15 coefficients per class',
        fontsize=13, fontweight='bold'
    )
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)

    st.markdown("""
    **Reading the coefficient chart:**
    A positive coefficient (red) increases the log-odds of that class.
    A negative coefficient (blue) decreases it. The magnitude indicates
    how strongly the feature influences the prediction.

    Note that `tuition_fees_up_to_date` appears as the strongest negative
    predictor for Dropout and the strongest positive predictor for Graduate --
    the same feature doing double duty, consistent with the EDA financial signals.
    """)