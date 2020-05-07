## Viberr

A music web application made using the Django framework with a PostgreSQL database, that allows you to upload and store music on the cloud. I developed this project as part of the onboarding process during my placement, using tutorials as a foundation and iterating upon it with more complex features designed by myself. Towards the end of the placement, I improved the project using the extra knowledge and experience gained during the year.

### Extra features
* User registration and authentication.
* Ability to 'favourite' songs, causes albums to sort with favourite songs displayed first.
* Displaying other albums from the same artist, which are conveniently hyperlinked.
* Adding songs to the database via file upload.
* Searching through albums & songs via database queries.

### Prerequisites
* Docker (version 19.03)
* docker-compose (version 1.25)

### How to use this repository
* Clone the repo to your device and navigate into it.
* Create a file called `.env` to store environment variables, e.g.
```
SECRET_KEY=foo
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```
* Build the docker image for the first time and spin up the container:  
```
docker-compose up --build
```
* You can now navigate to `localhost:8000` and access the website.

#### Useful commands
* An extension of Django's shell with autoloading of the app's database models is supported:
```
docker exec -it viberr_web_1 bash -c "python manage.py shell_plus"
```
* A series of tests covering most of the views can be used to verify the app works:  
```
docker exec -it viberr_web_1 bash -c "python3 manage.py test"
```
* When you create a new database, you might need to add a new admin user:
```
docker exec -it viberr_web_1 bash -c "python3 manage.py createsuperuser"
```

#### Troubleshooting
* When starting the Nginx container, there could be an error ending with "address already in use":
```
systemctl stop nginx
```

### Screenshots
* Here are two examples of pages accessible on viberr:
![Home Page](https://i.imgur.com/FrJNPK5.png)
![Songs](https://i.imgur.com/durTSd9.png)

### Acknowledgements
* 'Pacifico' font from [Google Fonts](https://fonts.google.com/specimen/Pacifico).
* Website favicon from [Font Awesome](https://fontawesome.com/icons/headphones-alt?style=solid).
* [Official Django documentation](https://docs.djangoproject.com/en/3.0/intro/tutorial01/)
* [thenewboston's Django youtube series](https://www.youtube.com/watch?v=qgGIqRFvFFk&list=PL6gx4Cwl9DGBlmzzFcLgDhKTTfNLfX1IK)
* [Tutorial on dockerising Django](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)

