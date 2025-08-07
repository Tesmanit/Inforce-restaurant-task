For more comfortable use you can use requirements.txt to install all the needed packages
Run python -m venv venv
Then run pip install -r requirements.txt
To start the whole project use docker-compose up --build if it wasn't build yet and if it was use docker-compose up
I provided some fixtures for faster testing
to load them use python manage.py loaddata fixtures.json
I also provided my testing insomnia collection, you can use it with your insonia application as well
To run automated tests use python manage.py test restaurant
Login and password for superuser is adminadmin

Passwords for all the employee users are employeeid{the number after employee username}
Passwords for all the restaurant users are restaurantid{the number after restaurant username}
JWT Token was used as auth tool, so use Bearer token authentication, it's in the Auth tab in Insomnia
To use flake8 run flake8 {app name(either employees or restaurant)}
For get request on http://localhost:8000/api/restaurant/votes/ you need to all header 'X-App-Version' (1 or 2)

You will also need to create .env file in app folder and fill it like that(you can use these exact values):
POSTGRES_DB=INFORCEDB
POSTGRES_USER=INFORCEUSER
POSTGRES_PASSWORD=INFORCEPASS