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

The database used is Postgres, also celery is used for background tasks and redis is used for communication between django and celery  
