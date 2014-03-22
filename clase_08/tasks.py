from celery import Celery
from celery.decorators import periodic_task
from celery.schedules import crontab

from datetime import datetime


celery = Celery('tasks')
celery.config_from_object('celeryconfig')


@celery.task
def sum(x, y):
    return x + y


@celery.task
def email():
    pass


@periodic_task(run_every=crontab())
def prueba():
    return datetime.now()
