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
        -- surrogate key: md5 hash of combined macro indicators (DuckDB-native, no dbt_utils needed)
        md5(
            cast(unemployment_rate as varchar) || '|' ||
            cast(inflation_rate as varchar) || '|' ||
            cast(gdp as varchar)
        ) as economic_context_key
    from "student_dropout"."main_staging"."stg_students"
)

select
    economic_context_key,
    unemployment_rate,
    inflation_rate,
    gdp
from base