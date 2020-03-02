# The Rodan Stack

<img src="_static/nginx.svg" width=50px>
Nginx is the HTTP and reverse proxy server used to connect Rodan to Internet

<img src="_static/django.png" width=50px>
Django is the web framework that powers the Rodan API functionality

<img src="_static/celery.png" width=50px>
Celery is the task queue used by Rodan to distribute the tasks to the workers

<img src="_static/rabbitmq.png" width=50px>
RabbitMQ is the messaging broker used to connect Rodan server to Celery

<img src="_static/redis.svg" width=50px>
Redis is used as message broker for backend websocket messaging

<img src="_static/gunicorn.png" width=50px>
Gunicorn is used as the interface between Nginx and Django

<img src="_static/postgres.png" width=50px>
PostgreSQL is the database system used by Rodan