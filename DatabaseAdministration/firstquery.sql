SELECT 
    employees.employee_name,
    departments.department_name,
    AVG(salaries.salary_amount) AS average_salary
FROM 
    employees
JOIN 
    departments ON employees.department_id = departments.department_id
JOIN 
    salaries ON employees.employee_id = salaries.employee_id
WHERE 
    employees.hire_date < '2023-01-01'
GROUP BY 
    employees.employee_name, departments.department_name
HAVING 
    COUNT(salaries.salary_id) >= 2
ORDER BY 
    average_salary DESC;
