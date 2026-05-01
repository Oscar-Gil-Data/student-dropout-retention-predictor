
    
    

select
    student_key as unique_field,
    count(*) as n_records

from "student_dropout"."main_marts"."fct_enrollment_outcomes"
where student_key is not null
group by student_key
having count(*) > 1


