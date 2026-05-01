-- int_program_context.sql
-- Extracts course/program attributes from the student-level flat file.
-- Course is a property of the program, not the individual student.

with base as (
    select distinct
        course_id,
        attendance_type,
        {{ dbt_utils.generate_surrogate_key([
            'course_id',
            'attendance_type'
        ]) }} as program_key
    from {{ ref('stg_students') }}
)

select
    program_key,
    course_id,
    attendance_type,
    case attendance_type
        when 1 then 'Daytime'
        when 0 then 'Evening'
        else 'Unknown'
    end as attendance_label,
    case course_id
        when 33    then 'Biofuel Production Technologies'
        when 171   then 'Animation and Multimedia Design'
        when 8014  then 'Social Service (evening)'
        when 9003  then 'Agronomy'
        when 9070  then 'Communication Design'
        when 9085  then 'Veterinary Nursing'
        when 9119  then 'Informatics Engineering'
        when 9130  then 'Equinculture'
        when 9147  then 'Management'
        when 9238  then 'Social Service'
        when 9254  then 'Tourism'
        when 9500  then 'Nursing'
        when 9556  then 'Oral Hygiene'
        when 9670  then 'Advertising and Marketing Management'
        when 9773  then 'Journalism and Communication'
        when 9853  then 'Basic Education'
        when 9991  then 'Management (evening)'
        else 'Other'
    end as course_name
from base
