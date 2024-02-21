WITH latest_orders AS (
    SELECT 
        customer_id,
        MAX(order_date) AS latest_order_date
    FROM 
        orders
    GROUP BY 
        customer_id
)

SELECT 
    customers.customer_name,
    COUNT(orders.order_id) AS total_orders,
    MAX(latest_orders.latest_order_date) AS last_order_date
FROM 
    customers
JOIN 
    orders ON customers.customer_id = orders.customer_id
JOIN 
    latest_orders ON customers.customer_id = latest_orders.customer_id
WHERE 
    orders.order_status = 'Shipped'
GROUP BY 
    customers.customer_name
HAVING 
    total_orders > 3
ORDER BY 
    last_order_date DESC;
