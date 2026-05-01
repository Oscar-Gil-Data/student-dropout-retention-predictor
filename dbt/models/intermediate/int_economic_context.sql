-- int_economic_context.sql
-- Extracts macroeconomic features into their own grain.
-- These are period-level attributes shared across students —
-- keeping them in the fact table would be semantically incorrect
-- and redundant across thousands of rows.

with base as (
    select distinct
        unemployment_rate,
        inflation_rate,
        gdp,
        -- surrogate key: economic periods are identified by the combination
        -- of all three macro indicators in this dataset
        {{ dbt_utils.generate_surrogate_key([
            'unemployment_rate',
            'inflation_rate',
            'gdp'
        ]) }} as economic_context_key
    from {{ ref('stg_students') }}
)

select
    economic_context_key,
    unemployment_rate,
    inflation_rate,
    gdp
from base
