# Microservice API Demo

## Tech Stack:
* Python 3.6
* Flask
* MongoDB
* gunicorn
* pytest
* dockerize
* Docker

## Approach:

* API and database components run in separate docker containers
* On startup the db container is initialized with data from the challenge in `init-db.js`
* The additional fields are updated on/de-serialized from database by the `/bmi-records` endpoint
* pytest is executed once the db and then the API containers are up, through [dockerize](https://github.com/jwilder/dockerize)
* If the tests are successful, the unittests container exits with a status code of 0
* The use of an ORM/ODM has been purposefully avoided due to performance overheads

## Endpoints

1. `/bmi-records` solves the first challenge
2. `/obesity-data` solves the second challenge, additionally the integrity of this endpoint's 
response is tested on test_views.test_validate_obesity_data
3. `/add-patient-data` sample data provided does not end up providing low enough BMI values
hence this POST endpoint was added for easier analysis

## Steps to run:

Docker and docker-compose are the only tools that need to be pre-installed.

Open a Terminal window and execute the following

### Clone Git repo and change directory

- `git clone git@github.com:saltgen/code-20210620-sagnikdutta.git`
- `cd code-20210620-sagnikdutta/`

### Initiate the relevant containers
- `docker-compose up`
    
Test container - unittests, will exit with a status code of 0 if all tests pass, pytest results will also be present on stdout.

The API service should be reachable on http://127.0.0.1:5000 or http://localhost:5000 at this point.

## Notes:

A Postman collection,`api_requests.postman_collection.json`, has been added to this repo to enable faster testing, feel free to update the hostnames if required.
  
A web-server such as nginx has not been added on top of gunicorn, as such a solution would eventually
find its way into something like Kubernetes. Through tools like ingress found in Kubernetes, the need for a web-server is eradicated.