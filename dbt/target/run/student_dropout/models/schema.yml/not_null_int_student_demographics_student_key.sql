
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select student_key
from "student_dropout"."main_intermediate"."int_student_demographics"
where student_key is null



  
  
      
    ) dbt_internal_test