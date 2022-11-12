# products_api

The project environement variables to be stored in .env file at the same directory as settings.py file, the file should contain these variables   

SECRET_KEY=django_sectet_key    
POSTGRES_DB=database_name  
POSTGRES_USER=user   
POSTGRES_PASSWORD=Password   

This API is runnable in Docker using these commands  
  - docker-compose build   
  - docker-compose up  
  
to start the terminal inside Docker   
  - docker exec -it products_api_container /bin/bash  
  
API documentation can be accessed using this endpoint: http://localhost:8000/api/schema/swagger-ui/

The database used is Postgres, also celery is used for background tasks and redis is used as a message broker.   

This API is used to:   
1. receive the product feed (products.json), normalize it, and store it in a PostgreSQL database.
2. return the stored product info individually (by code) or the entire range as an array if no argument is passed.


Hints:   
1. Products are identified using the field `code` in combination with the field `type`.    
2. The `code` field should not contain any leading zeros once it is stored in our database.     
3. The `code` may be a mix of both, ones with leading zeros and without them.    
4. There may be unicode characters which need to be parsed before storing in our database.    
5. The field `trade_item_unit_descriptor` may also be present as `trade_item_descriptor` but should be transformed to the first before being stored in the DB.     
