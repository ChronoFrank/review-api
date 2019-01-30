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


Happy coding :)
