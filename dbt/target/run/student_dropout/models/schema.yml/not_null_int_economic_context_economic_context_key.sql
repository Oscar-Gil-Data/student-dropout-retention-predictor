
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select economic_context_key
from "student_dropout"."main_intermediate"."int_economic_context"
where economic_context_key is null



  
  
      
    ) dbt_internal_test