-- fct_enrollment_outcomes.sql
-- Fact table at student grain.
-- Holds academic performance metrics, foreign keys to dimensions, and the outcome target.

with students as (
    select
        row_number() over () as student_key,
        *
    from {{ ref('stg_students') }}
),

program_keys as (
    select * from {{ ref('int_program_context') }}
),

economic_keys as (
    select * from {{ ref('int_economic_context') }}
)

select
    -- keys
    s.student_key,
    p.program_key,
    e.economic_context_key,

    -- enrollment context
    s.application_mode,
    s.application_order,
    s.previous_qualification,
    s.previous_qualification_grade,
    s.admission_grade,

    -- financial
    s.is_scholarship_holder,
    s.tuition_fees_up_to_date,
    s.is_debtor,

    -- semester 1 performance
    s.sem1_units_credited,
    s.sem1_units_enrolled,
    s.sem1_evaluations,
    s.sem1_units_approved,
    s.sem1_grade,
    s.sem1_units_no_eval,

    -- semester 2 performance
    s.sem2_units_credited,
    s.sem2_units_enrolled,
    s.sem2_evaluations,
    s.sem2_units_approved,
    s.sem2_grade,
    s.sem2_units_no_eval,

    -- derived metrics
    safe_divide(s.sem1_units_approved, nullif(s.sem1_units_enrolled, 0)) as sem1_approval_rate,
    safe_divide(s.sem2_units_approved, nullif(s.sem2_units_enrolled, 0)) as sem2_approval_rate,

    -- target
    s.outcome

from students s
left join program_keys p
    on p.course_id = s.course_id
    and p.attendance_type = s.attendance_type
left join economic_keys e
    on e.unemployment_rate = s.unemployment_rate
    and e.inflation_rate = s.inflation_rate
    and e.gdp = s.gdp
