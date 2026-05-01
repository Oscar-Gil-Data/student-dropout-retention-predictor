
  
  create view "student_dropout"."main_intermediate"."int_student_demographics__dbt_tmp" as (
    -- int_student_demographics.sql
-- Isolates student-level demographic and household attributes.
-- These describe the student, not the enrollment event.

with base as (
    select
        -- student identifier (row number as surrogate — no natural key in dataset)
        row_number() over () as student_key,
        nationality,
        gender,
        age_at_enrollment,
        is_international,
        is_displaced,
        has_special_needs,
        marital_status,
        mothers_qualification,
        fathers_qualification,
        mothers_occupation,
        fathers_occupation
    from "student_dropout"."main_staging"."stg_students"
)

select
    student_key,
    nationality,
    gender,
    case gender
        when 1 then 'Male'
        when 0 then 'Female'
        else 'Unknown'
    end as gender_label,
    age_at_enrollment,
    is_international,
    is_displaced,
    has_special_needs,
    marital_status,
    case marital_status
        when 1 then 'Single'
        when 2 then 'Married'
        when 3 then 'Widower'
        when 4 then 'Divorced'
        when 5 then 'Facto union'
        when 6 then 'Legally separated'
        else 'Unknown'
    end as marital_status_label,
    mothers_qualification,
    fathers_qualification,
    mothers_occupation,
    fathers_occupation
from base
  );
