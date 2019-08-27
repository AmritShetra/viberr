## viberr
A music application made using Django, with a PostgreSQL database, that allows you to upload and store your music on the cloud. I developed this as part of the developer onboarding process at Reckon Digital, as I set out to become familiar with the technologies used. I read the official Django documentation, along with thenewboston's Django tutorial video series to create the initial version of this, then decided to try and create extra features myself.

### Extra features, you say?
* User registration and authentication.
* Ability to 'favourite' songs - this causes albums to be sorted with favourite songs displayed first.
* Displaying other albums from the artist, which are conveniently hyperlinked.
* Adding songs to the database.
* Searching through albums/songs, which runs a query to look through the database.

### How to use this repository
* Clone the repo to your device and run ```sudo docker-compose up```.  
* Run ```sudo docker exec -it viberr_postgres_1 bash```, then ```su postgres``` and finally, ```psql``` to access the PostgreSQL database.  
* Run ```sudo docker exec -it viberr_viberr_1 bash -c "python3 manage.py shell"``` to access the shell.  

