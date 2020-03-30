## viberr
A music web application made using Django, with a PostgreSQL database, that allows you to upload and store your music on the cloud. I developed this as part of the developer onboarding process at Reckon Digital, as I set out to become familiar with the technologies used. I read the [official Django documentation](https://docs.djangoproject.com/en/2.2/intro/tutorial01/), along with [thenewboston's Django tutorial video series](https://www.youtube.com/watch?v=qgGIqRFvFFk&list=PL6gx4Cwl9DGBlmzzFcLgDhKTTfNLfX1IK) to create the initial version of this, then decided to try and create extra features myself.

### Prerequisites
* Docker (at time of writing, used version 18.09.7)
* docker-compose (at time of writing, used version 1.21.0)

### Extra features, you say?
* User registration and authentication.
* Ability to 'favourite' songs - this causes albums to be sorted with favourite songs displayed first.
* Displaying other albums from the artist, which are conveniently hyperlinked.
* Adding songs to the database.
* Searching through albums/songs, which runs a query to look through the database.

### How to use this repository
* Clone the repo to your device and build the docker image for the first time:  
```
sudo docker-compose up --build
```

* This command is used so that the website can access static files (e.g. CSS):
```
sudo docker exec viberr_django_1 bash -c "python3 manage.py collectstatic"
```

* After this, you only need to run the following command each time you run the server:  
```
sudo docker-compose up
```
* The following commands can be used to access PostgreSQL:  
```
sudo docker exec -it viberr_postgres_1 bash  
su postgres  
psql
```
* You can then add a new database and connect to it (then use normal SQL to view tables etc.):
```
CREATE DATABASE viberr_db;
\c viberr_db
```
* To access the shell, you have to enter the container and access the terminal:  
```
sudo docker exec -it viberr_django_1 bash -c "python3 manage.py shell"
```
* A very similar command can be used to run tests:  
```
sudo docker exec -it viberr_django_1 bash -c "python3 manage.py test"
```
* When you create a new database, you might need to add a new admin user:
```
sudo docker exec -it viberr_django_1 bash -c "python3 manage.py createsuperuser"
```

### Troubleshooting
* When starting the Nginx container, there might be an error ending with "address already in use":
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