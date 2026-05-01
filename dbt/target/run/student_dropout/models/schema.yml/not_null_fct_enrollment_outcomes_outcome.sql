
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select outcome
from "student_dropout"."main_marts"."fct_enrollment_outcomes"
where outcome is null



  
  
      
    ) dbt_internal_test