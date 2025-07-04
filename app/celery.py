from celery import Celery

celery_app = Celery("journey_app")
celery_app.config_from_object("app.celeryconfig")