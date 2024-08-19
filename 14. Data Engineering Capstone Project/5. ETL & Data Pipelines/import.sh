psql -h 172.21.247.1 -U postgres -d sales -p 5432 -W 9rByRHD9xA0znXBPjIuS1frP << EOF
\copy sales_data(product_id, customer_id, quantity, timestamp) 
FROM 'sales.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"', ESCAPE '"', NULL '');
EOF

psql -h 172.21.247.1 -U postgres -d sales -p 5432 -W 9rByRHD9xA0znXBPjIuS1frP