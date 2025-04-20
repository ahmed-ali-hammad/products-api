<h3 align="center">Products API</h3>

<div align="center">
  <img src="https://img.shields.io/badge/status-active-success.svg" />
  <img src="https://img.shields.io/badge/python-3.13-blue" />
</div>

---

<p align="center">products-api
    <br> 
</p>

## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting-started)
- [Built Using](#built-using)

## 🧐 About <a name = "about"></a>
This API is used to:   
1. receive the product feed (products.json), normalize it, and store it in a PostgreSQL database.
2. return the stored product info individually (by code) or the entire range as an array if no argument is passed.


Hints:   
1. Products are identified using the field `code` in combination with the field `type`.    
2. The `code` field should not contain any leading zeros once it is stored in our database.     
3. The `code` may be a mix of both, ones with leading zeros and without them.    
4. There may be unicode characters which need to be parsed before storing in our database.    
5. The field `trade_item_unit_descriptor` may also be present as `trade_item_descriptor` but should be transformed to the first before being stored in the DB.

## 🏁 Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites
 - [Docker](https://docs.docker.com/)
 - [Docker Compose](https://docs.docker.com/compose/)

### Installing
If you're opening this project using [devcontainers](https://containers.dev/) then your docker container should be ready to go!

Otherwise you will need to start the docker compose environment `docker compose up` and open a shell into the container `products_api_container`.

```bash
$ docker compose up
$ docker exec -it products_api_container sh  # spawns a shell within the docker container
$ pipenv shell  # spawns a shell within the virtualenv 
```

### ▶️ Running the API
```bash
$ python3 products_api/manage.py runserver 0.0.0.0:8000
```

Endpoints:
- [API Docs](http://localhost:8000/api/schema/swagger-ui/)

### 🧪 Running the tests <a name = "tests"></a>
- [pytest](https://docs.pytest.org/) is used to run unit and integration tests.   

🚧 Work in Progress

### Code Style & Linting
The following tools are run during pipelines to enforce code style and quality.

 - [flake8](https://flake8.pycqa.org/en/latest/) for linting
 - [isort](https://pycqa.github.io/isort/) for import sorting
 - [black](https://black.readthedocs.io/en/stable/) for code style

### Python Package Management
- [pipenv](https://pipenv.pypa.io/en/latest/) is used to manage Python packages. 

```bash
$ pipenv shell  # spawns a shell within the virtualenv
$ pipenv install  # installs all packages from Pipfile
$ pipenv install --dev # installs all packages from Pipfile, including dev dependencies
$ pipenv install <package1> <package2>  # installs provided packages and adds them to Pipfile
$ pipenv update  # update package versions in Pipfile.lock, this should be run frequently to keep packages up to date
$ pipenv uninstall package # uninstall a package 
$ pipenv uninstall package  --categories dev-packages # uninstall a dev package
```

## ⛏️ Built Using <a name = "built_using"></a>
- [Django](https://www.djangoproject.com/) - Web Framework.
- [PostgreSQL](https://www.postgresql.org/) - Database.
- [Celery](https://docs.celeryq.dev/en/stable/) - Distributed Task Queue.
- [Redis](https://redis.io/) - Message Broker.