
## Synopsis

Propygate: A small Django Web app meant to be launched on a raspberry pi for monitoring seed/seedling/plant environment conditions (Heat and light only right now).

## Motivation

Hot pepper seeds (for example) can be hard to germinate. This program is designed to help create the ideal environment for any home grown plant.

## Installation

Propygate uses the following (and more):

	Django
	Celery
	RPi.GPIO
	Redis server
	Apache2 web server

**Basic setup:**

	clone this repo
	pip install -r requirements.txt
	Install [Redis](https://redis.io/topics/quickstart)
	apt-get install apache2
	service apache2 restart
	Configure some enviros.
	redis-server <path to redis.conf>
	python manage.py celery beat
	python manage.py celery worker

## Tests

None yet

## Contributors

Ryan Bottema
