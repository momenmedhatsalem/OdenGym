# tasks.py

from celery import shared_task
from django.utils import timezone
from .models import Membership

@shared_task
def update_membership_validity():
    memberships = Membership.objects.filter(paid=False)
    for membership in memberships:
        if membership.valid_date < timezone.now():
            membership.valid = False
            membership.save()


