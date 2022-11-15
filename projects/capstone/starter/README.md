
CAPSTONE PROJECT- CASTING AGENCY
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 

MODELS
Movies with attributes title and release date
Actors with attributes name, age and gender

AUNTHENTICATION
RBAC has been used. Depending on the role the authentication and access is provided. I have used JWT token based authentication with OAuth.
Roles:
Casting Assistant
    Can view actors and movies
Casting Director
    All permissions a Casting Assistant has and…
    Add or delete an actor from the database
    Modify actors or movies
Executive Producer
    All permissions a Casting Director has and…
    Add or delete a movie from the database

APPLICATION HOSTED URL: https://capstone483new.herokuapp.com/

ENDPOINTS
1. GET MOVIES
URL: https://capstone483new.herokuapp.com/movies
RESPONSE:
{
    "movies": [
        {
            "id": 1,
            "releasedate": "2014",
            "title": "HP"
        }
    ],
    "success": true,
    "total_movies": 1
}

2. POST MOVIES
URL: https://capstone483new.herokuapp.com/movies
REQUEST:
{
    "title": "HP",
    "releasedate": 2014
}
RESPONSE:
{
    "movie": [
        {
            "id": 1,
            "releasedate": "2015",
            "title": "Wolverine"
        },
        {
            "id": 2,
            "releasedate": "2014",
            "title": "HP"
        }
    ],
    "success": true,
    "total_movie": 2
}

3. PATCH MOVIES
URL: https://capstone483new.herokuapp.com/movies/<movie_id>
REQUEST:
{
            "releasedate": 2014,
            "title": "HP new"
        }
RESPONSE:
{
    "id": 2,
    "releasedate": "2014",
    "title": "HP new"
}

4. DELETE MOVIES
URL: https://capstone483new.herokuapp.com/movies<movie_id>
RESPONSE:
{
    "current_movies": [
        {
            "id": 2,
            "releasedate": "2014",
            "title ": "HP"
        }
    ],
    "deleted": 1,
    "success": true,
    "total_movies": 1
}

5. GET ACTORS
URL: https://capstone483new.herokuapp.com/actors
RESPONSE:
{
    "actors": [
        {
            "age": 30,
            "gender": "M",
            "id": 1,
            "name ": "Bing"
        }
    ],
    "success": true,
    "total_actors": 1
}

6. POST ACTORS
URL: https://capstone483new.herokuapp.com/actors
REQUEST:
{"name":"Bing",
"age":30,
"gender":"M"}

RESPONSE:
{
    "actors": [
        {
            "age": 30,
            "gender": "M",
            "id": 1,
            "name ": "Bing"
        }
    ],
    "success": true,
    "total_actors": 1
}


7. PATCH ACTORS
URL: https://capstone483new.herokuapp.com/actors/<actor_id>
REQUEST:
{"name":"Muriel",
"age":30,
"gender":"M"}
RESPONSE:
{
    "age": 30,
    "gender": "M",
    "id": 2,
    "name ": "Muriel"
}

8. DELETE ACTORS
URL: https://capstone483new.herokuapp.com/actors/<actor_id>
RESPONSE:
{
    "current_actors": [
        {
            "age": 30,
            "gender": "M",
            "id": 1,
            "name ": "abby"
        }
    ],
    "deleted": 4,
    "success": true,
    "total_actors": 1
}

INSTALLING DEPENDENCIES
pip install -r requirements.txt

RUN APP IN LOCAL
python app.py

DATABASE MIGRATION 

python manage.py db init
python manage.py db migrate -m "Initial migration"
python manage.py db upgrade