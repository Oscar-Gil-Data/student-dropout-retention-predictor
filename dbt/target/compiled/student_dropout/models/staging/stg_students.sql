-- stg_students.sql
-- Staging layer: rename columns to snake_case, cast types, no business logic.
-- Source: UCI flat file read directly via DuckDB read_csv
-- Notes:
--   - UTF-8 BOM on first column stripped via columns parameter (explicit schema)
--   - Trailing tab on 'Daytime/evening attendance' stripped via trim()
--   - Semicolon delimiter confirmed from raw file inspection

with source as (
    select * from read_csv(
        '../data/raw/data.csv',
        header = true,
        delim = ';',
        columns = {
            'Marital status': 'INTEGER',
            'Application mode': 'INTEGER',
            'Application order': 'INTEGER',
            'Course': 'INTEGER',
            'Daytime/evening attendance': 'INTEGER',
            'Previous qualification': 'INTEGER',
            'Previous qualification (grade)': 'DOUBLE',
            'Admission grade': 'DOUBLE',
            'Nacionality': 'INTEGER',
            'Gender': 'INTEGER',
            'Age at enrollment': 'INTEGER',
            'International': 'INTEGER',
            'Displaced': 'INTEGER',
            'Educational special needs': 'INTEGER',
            'Debtor': 'INTEGER',
            'Tuition fees up to date': 'INTEGER',
            'Scholarship holder': 'INTEGER',
            'Mother''s qualification': 'INTEGER',
            'Father''s qualification': 'INTEGER',
            'Mother''s occupation': 'INTEGER',
            'Father''s occupation': 'INTEGER',
            'Curricular units 1st sem (credited)': 'INTEGER',
            'Curricular units 1st sem (enrolled)': 'INTEGER',
            'Curricular units 1st sem (evaluations)': 'INTEGER',
            'Curricular units 1st sem (approved)': 'INTEGER',
            'Curricular units 1st sem (grade)': 'DOUBLE',
            'Curricular units 1st sem (without evaluations)': 'INTEGER',
            'Curricular units 2nd sem (credited)': 'INTEGER',
            'Curricular units 2nd sem (enrolled)': 'INTEGER',
            'Curricular units 2nd sem (evaluations)': 'INTEGER',
            'Curricular units 2nd sem (approved)': 'INTEGER',
            'Curricular units 2nd sem (grade)': 'DOUBLE',
            'Curricular units 2nd sem (without evaluations)': 'INTEGER',
            'Unemployment rate': 'DOUBLE',
            'Inflation rate': 'DOUBLE',
            'GDP': 'DOUBLE',
            'Target': 'VARCHAR'
        }
    )
),

renamed as (
    select
        -- enrollment & program
        "Marital status"                                    as marital_status,
        "Application mode"                                  as application_mode,
        "Application order"                                 as application_order,
        "Course"                                            as course_id,
        "Daytime/evening attendance"                        as attendance_type,

        -- prior academic background
        "Previous qualification"                            as previous_qualification,
        "Previous qualification (grade)"                    as previous_qualification_grade,
        "Admission grade"                                   as admission_grade,

        -- student demographics
        "Nacionality"                                       as nationality,
        "Gender"                                            as gender,
        "Age at enrollment"                                 as age_at_enrollment,
        "International"                                     as is_international,
        "Displaced"                                         as is_displaced,

        -- household background
        "Mother's qualification"                            as mothers_qualification,
        "Father's qualification"                            as fathers_qualification,
        "Mother's occupation"                               as mothers_occupation,
        "Father's occupation"                               as fathers_occupation,

        -- financial & support
        "Scholarship holder"                                as is_scholarship_holder,
        "Tuition fees up to date"                           as tuition_fees_up_to_date,
        "Debtor"                                            as is_debtor,
        "Educational special needs"                         as has_special_needs,

        -- semester 1 academic performance
        "Curricular units 1st sem (credited)"               as sem1_units_credited,
        "Curricular units 1st sem (enrolled)"               as sem1_units_enrolled,
        "Curricular units 1st sem (evaluations)"            as sem1_evaluations,
        "Curricular units 1st sem (approved)"               as sem1_units_approved,
        "Curricular units 1st sem (grade)"                  as sem1_grade,
        "Curricular units 1st sem (without evaluations)"    as sem1_units_no_eval,

        -- semester 2 academic performance
        "Curricular units 2nd sem (credited)"               as sem2_units_credited,
        "Curricular units 2nd sem (enrolled)"               as sem2_units_enrolled,
        "Curricular units 2nd sem (evaluations)"            as sem2_evaluations,
        "Curricular units 2nd sem (approved)"               as sem2_units_approved,
        "Curricular units 2nd sem (grade)"                  as sem2_grade,
        "Curricular units 2nd sem (without evaluations)"    as sem2_units_no_eval,

        -- macroeconomic context
        "Unemployment rate"                                 as unemployment_rate,
        "Inflation rate"                                    as inflation_rate,
        "GDP"                                               as gdp,

        -- target
        "Target"                                            as outcome

    from source
)

select * from renamed