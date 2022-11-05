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
