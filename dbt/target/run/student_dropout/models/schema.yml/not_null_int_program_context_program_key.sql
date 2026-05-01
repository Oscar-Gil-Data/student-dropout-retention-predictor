
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select program_key
from "student_dropout"."main_intermediate"."int_program_context"
where program_key is null



  
  
      
    ) dbt_internal_test