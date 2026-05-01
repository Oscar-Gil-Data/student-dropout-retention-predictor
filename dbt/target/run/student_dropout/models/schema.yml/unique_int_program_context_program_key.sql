
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    program_key as unique_field,
    count(*) as n_records

from "student_dropout"."main_intermediate"."int_program_context"
where program_key is not null
group by program_key
having count(*) > 1



  
  
      
    ) dbt_internal_test