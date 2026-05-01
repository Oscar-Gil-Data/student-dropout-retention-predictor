
    
    

with all_values as (

    select
        outcome as value_field,
        count(*) as n_records

    from "student_dropout"."main_marts"."fct_enrollment_outcomes"
    group by outcome

)

select *
from all_values
where value_field not in (
    'Dropout','Enrolled','Graduate'
)


