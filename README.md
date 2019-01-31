# Review API Service

## Instructions for development:

#### 1. Create virtualenv:
```
mkvirtualenv review_api
```
#### 2. Link project dir to postactivate:
```
setvirtualenvproject <project_dir>
```
#### 3. Clone the repository:
```
git clone git@github.com:ChronoFrank/review-api.git 

or 

git clone https://github.com/ChronoFrank/review-api.git
```
#### 4. Install dependencies:
```
workon review_api
pip install -r requirements.txt
```
#### 5. Migrate the database (PostgreSQL):

Switch to the `postgres` user.

```
sudo su postgres
```

Create database user `reviewapi` with password `reviewapi`.

```
createuser -U postgres -s -P reviewapi
```

Create a database named `reviewapi`.

```
createdb -U reviewapi reviewapi
```

Then you can sync the database with your own user.

```
workon review_api
python manage.py migrate
```

#### 6. Run tests to validate everything
```
workon profiles
python manage.py test

# if we want to get the coverage report:
coverage run manage.py test; coverage report -m; coverage html -d cover/
```
#### 7. Run the server:
```
$ python manage.py runserver
```

the api documentation is at http://localhost:8000/docs


#### 8. Usage
first you will have to create a user, using the following request.
All the fields in the payload are mandatory.
```
curl -X POST \
  http://localhost:9000/api/v1/users/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
	"username": "test",
	"first_name": "test",
	"last_name": "test",
	"email": "test@mailinator.com",
	"password": "123456"
}'

```

once the user is created, 
you will have to generate an access token so you can authenticate to the other enpoints 

```
#### request ##### 
curl -X POST \
  http://localhost:8000/api/v1/access_token/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{"username": "test", "password":"123456"}'
  
#### Response ####

{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwidXNlcl9pZCI6MTIsImp0aSI6IjI5OGRjYTExODAxZDRkMzhiYmM0NDZiYmJkYWRlOTcwIiwiZXhwIjoxNTQ4OTcxODcyfQ.pIKY3NBsRxbk1luzyxUYucyHKKnnori0e3TI26DvZzw",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsInVzZXJfaWQiOjEyLCJqdGkiOiI5NTc5Y2NlMDVmOTI0OGI4YTIxMzZhM2Q2OGU2MTdkNSIsImV4cCI6MTU0OTA1NzY3Mn0.84HpReGRRaJYe50R-OIO-jYzHhZ2mbgKT074J1_bu-I"
}
```

Now you can use the access_token to create and retrive reviews, using the following endpoints.

```
#### REQUEST ####

curl -X GET \
  http://localhost:8000/api/v1/reviews/ \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwidXNlcl9pZCI6MTIsImp0aSI6IjI5OGRjYTExODAxZDRkMzhiYmM0NDZiYmJkYWRlOTcwIiwiZXhwIjoxNTQ4OTcxODcyfQ.pIKY3NBsRxbk1luzyxUYucyHKKnnori0e3TI26DvZzw' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache'
  
 
### RESPONSE ###
 [
    {
        "reviewer_name": "test",
        "title": "this is a review title",
        "rating": 4,
        "company_name": "fake company",
        "summary": "this is a sumary review",
        "submission_date": "2019-01-29T23:35:22.786259Z",
        "ip_address": "127.0.0.1"
    }
]
  

```


```
### REQUEST ###

curl -X POST \
  http://localhost:9000/api/v1/reviews/ \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwidXNlcl9pZCI6MTIsImp0aSI6ImFhNjczZDg0MzJkNzRjM2U5ZGYxMmNhY2M4MTYwNGNjIiwiZXhwIjoxNTQ4OTcyNjAyfQ.lWCVt-Qwx_V3PHHFKhXYDGOcPYjI0VMfHilu7ow_s_Q' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
	"title": "new review test",
	"rating": 4,
	"company_name": "fake company",
	"summary": "this is a sumary test review"
}'

### RESPONSE ###
{
    "reviewer_name": "test",
    "title": "new review test",
	"rating": 4,
	"company_name": "fake company",
	"summary": "this is a sumary test review"
    "submission_date": "2019-01-31T22:00:25.592424Z",
    "ip_address": "127.0.0.1"
}
```


Happy coding :)
