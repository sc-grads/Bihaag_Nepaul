CREATE USER ecomuser WITH PASSWORD 'ecompassword';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecomuser;
ALTER DATABASE ecommerce_db OWNER TO ecomuser;