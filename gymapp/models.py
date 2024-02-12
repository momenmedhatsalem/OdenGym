
from django.db import models

from django.db.models.signals import *
from django.dispatch import receiver

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TRAINER = 'TR'
    CUSTOMER = 'CU'
    MEMBER = 'ME'

    USER_TYPE_CHOICES = [
        (TRAINER, 'Trainer'),
        (CUSTOMER, 'Customer'),
        (MEMBER, 'Member'),
    ]

    user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES, default=CUSTOMER)



    def __str__(self):
        return self.username


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer')
    bio = models.TextField()
    expertise = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name()

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    # Add any other fields specific to members

    def __str__(self):
        return self.user.get_full_name()

@receiver(post_save, sender=User)
def user_post_save_function(sender, instance, created, *args, **kwargs):
     if created:
        if instance.user_type == 'TR':
            Trainer.objects.create(user=instance)
        elif instance.user_type == 'ME':
            Member.objects.create(user=instance)



class Class(models.Model):
    name = models.CharField(max_length=100)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name

class Schedule(models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.class_instance.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Booking(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.schedule.class_instance.name}"

class Membership(models.Model):
    DURATION_CHOICES = [
        ('monthly', 'Monthly'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('yearly', 'Yearly'),
    ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.get_duration_display()}"

class Attendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateField()
    location = models.CharField(max_length=255)  # Assuming you store location as a string for simplicity

    class Meta:
        unique_together = ['member', 'date']  # Ensures only one attendance record per member per day

    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.date}"
