
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        outcome as value_field,
        count(*) as n_records

    from "student_dropout"."main_staging"."stg_students"
    group by outcome

)

select *
from all_values
where value_field not in (
    'Dropout','Enrolled','Graduate'
)



  
  
      
    ) dbt_internal_test