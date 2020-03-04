from django.contrib.auth import get_user_model

from django_sample_project.django_sample_project import celery_app

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()
