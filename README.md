# Youtubefetch

* The server calls the YouTube API continuously in background with some interval (say ~1 minutes) for fetching the latest videos for a predefined search query and stores the data of videos in a postgres database with proper indexes.

* A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
A basic search 
* API to search the stored videos using their title and description.

* Dockerize the project.

* Add support for supplying multiple API keys so that if quota is exhausted on one, it automatically uses the next available key.

* Optimise search api, so that it's able to search videos containing partial match for the search query in either video title or description.


# Methods Used
* For calling youtube API , Have written a cron which would fetch the data at certain times and upload to DB. 

* For storing the data in DB, have created a trigger in Migrations which updates the searchvector field defined on title and description of video in models.py. This ensures that we never have to worry about the creation of these values.

* Have added GIN indexes as opposed to basic B-tree indexes as they outperform in case of FTS. 

* For Basic data fetching API, have used ```LimitOffsetPagination``` which is equivalent to Mongo DB skip and limit. Have added default ordering (```filters.OrderingFilter```)fields which supports sorting accross multiple fields. 

* For search API, have added the full text searches functionality of postgres which allows us quick partial searches. Also, have added Search Vectorr Field to models which precomputes these values on insertion or updation so that runtime searches are highly optimized.




# Methods to explore
* Although, django-celery is also available and would implement huey in the next iteration. Finalized huey because it is a lightweight solution to async tasks in python and is redis based which makes it significantly faster than celery and provides rock solid atomicity and stability.

 * Also tried using Trigram Similarity support which is equivalent to fuzzy search approach but it didn't work in case of description. We cannot use it here but i can be used if we require to search for single word or 2 words where in we need to also add the functionality of basic spell check. (For ex.- if we have to search for Asian as a cuisine and customer writes Asean, then the search results would match). This failed for long sentences. Search for FTS + Trigram(https://stackoverflow.com/questions/61451030/postgresql-text-search-in-django-not-working-as-expected, https://www.paulox.net/2017/12/22/full-text-search-in-django-with-postgresql/) didn't work 


  



## Installation

* Clone the project
* If your PC is not django ready, use [this](https://www.codingforentrepreneurs.com/blog/create-a-blank-django-project) 
* Install docker
* run ```docker-compose up --build -d``` for initial build and ```docker-compose up``` for subsequent ones.
* Make a .env with YOUTUBE_KEY='','','' (and so on) and 
DJANGO_SECRET_KEY=' in them
* For getting an API key follow [this](https://developers.google.com/youtube/v3/getting-started)
* Setup cron to run Job, Follow [this](https://django-cron.readthedocs.io/en/latest/installation.html)
* Run the server using 
```bash 
docker-compose up
```

Test cron commands
```bash
docker-compose run web python manage.py runcrons task.scheduler.fetchYoutubeVideoData
```

Management Commands
```bash
docker-compose run web python manage.py migrate
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

