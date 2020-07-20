# CSV Analyzer - General description

CSV Analyzer allows users to create multiple data sets giving a unique name for each one. Users can upload an excel 
file that contains weather data using the API.

It is built using Python, Django, Django Rest Framework, Celery, PostgreSQL as main database and **MongoDB**
as a database to store the data sets data (Data from files). 

Celery is used to execute the hard processing tasks, like analyzing the csv files for data sets.

> The API documentation with Swagger is available on `http://localhost:8000/swagger/`

## Project detail description

Data set API allows users to get the data sets, get a single dataset, create a data set and upload an excel file to
a data set.

When an excel file is uploaded into a dataset, it's not analyzed immediately, instead, the file is saved and created as
is_analyzed=False. A **Celery** task will run the job of analyzing and store the file information into MongoDB.

When the DataSet API (List or Retrieve) is called, the API will return the current state of the DataSet, including the 
data in MongoDB (if that exists).

###### PostgreSQL general model definition is:

    User ->
        | DataSet ->
            name: User's given name.
            owner: User object relationship.
            is_analyzed: Boolean.
            
            *-> DataSetFiles (OneToMany)
                -> file: FileField.
                -> data_set: DataSet object relationship.
                -> is_analyzed: Boolean.

###### MongoDB structure definition
    {
        "data_set_id": "54c49b1e-8901-435b-9a95-2ecf5a16a415",
        "data_set_file_id": "8e25efb7-4d29-4038-9f28-264d1f8e8964",
        "number": 0,
        "air_pressure_9am": 918.060000000008,
        "air_temp_9am": 74.8220000000004,
        "avg_wind_direction_9am": 271.1,
        "avg_wind_speed_9am": 2.08035419999976,
        "max_wind_direction_9am": 295.399999999999,
        "max_wind_speed_9am": 2.8632831999999,
        "rain_accumulation_9am": 0,
        "rain_duration_9am": 0,
        "relative_humidity_9am": 42.4200000000004,
        "relative_humidity_3pm": 36.1600000000004
    }


## Basic Commands

Steps to run the complete environment locally (Django, PostgreSQL, Celery, Redis and MongoDB).

    docker-compose -f local.yml build
    
    docker-compose -f local.yml up
    
> Now the app will be running on port 8000.


## Test coverage

You can run all unit test with the next command:

`docker-compose run --rm django coverage run -m pytest`


## API Endpoints

You can see the API endpoints using the swagger utils on `/swagger/`, also looking the Postman collection in the repo.

(I really recommend take a look to postman collection, is the easier way to test).

*Note: -> Remember replace the file for Postman in "Create dataset file with your local file.*

### Authentication

Login -> `[POST] /api/auth/users/`

    {
        "username": "test1@mail.com",
        "password": "abcd1234."
    }
    
SignUp -> `[POST] /api/auth/jwt/create/`

    {
        "username": "test1@mail.com",
        "password": "abcd1234."
    }
    
### Datasets

Get User's DataSets -> `[GET] /api/dataset/`

Get a DataSet -> `[GET] /api/dataset/{data-set-id}`

Create a DataSet -> `[POST] /api/dataset/`

    {
        "name": "Something"
    }

Create a DataSet File `[POST] /api/dataset/{data-set-id}/add-file/`

    {
        "file": YourFileObject (You can found an example on Postman Collection).
    }