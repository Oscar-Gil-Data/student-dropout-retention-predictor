
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    economic_context_key as unique_field,
    count(*) as n_records

from "student_dropout"."main_intermediate"."int_economic_context"
where economic_context_key is not null
group by economic_context_key
having count(*) > 1



  
  
      
    ) dbt_internal_test