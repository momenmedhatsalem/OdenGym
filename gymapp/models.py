
from django.db import models

from django.db.models.signals import *
from django.dispatch import receiver
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

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

@receiver(pre_save, sender=User)
def validate_user_type(sender, instance, **kwargs):

    if instance.user_type not in [choice[0] for choice in instance.USER_TYPE_CHOICES]:
        raise ValueError("Invalid user type")


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer')
    bio = models.TextField()
    expertise = models.CharField(max_length=100)
    instagram = models.URLField(blank=True, null=True)
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
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Class)
def validate_user_type(sender, instance, **kwargs):

    if instance.trainer.user_type != User.TRAINER:
        raise ValueError("Invalid user type")


# class Schedule(models.Model):
#     class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()

#     def __str__(self):
#         return f"{self.class_instance.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

# class Booking(models.Model):
#     member = models.ForeignKey(User, on_delete=models.CASCADE)
#     newClass = models.ForeignKey(Class, on_delete=models.CASCADE, default=None)

#     def __str__(self):
#         return f"{self.member.user.get_full_name()} - {self.newClass.name}"

class Membership(models.Model):
    DURATION_CHOICES = [
        (30, 'Monthly'),  # 30 days for monthly
        (90, '3 Months'), # 90 days for 3 months
        (180, '6 Months'), # 180 days for 6 months
        (365, 'Yearly'),  # 365 days for yearly
    ]
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.IntegerField(choices=DURATION_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    valid_date = models.DateField(blank=True, null=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        # Assuming Member model has a user attribute
        return f"{self.member.username} - {self.duration}"

@receiver(post_save, sender=Membership)
def Membership_post_save_function(sender, instance, created, *args, **kwargs):
     if created and instance.paid == False:
        instance.valid_date = instance.start_date + timedelta(days=3)
        instance.end_date = instance.start_date + timedelta(days=instance.duration)
        
        instance.save()
        # send email to the user
@receiver(pre_save, sender=Membership)
def validate_user_type(sender, instance, **kwargs):

    if instance.member.user_type != User.MEMBER:
        raise ValueError("Invalid user type")    



class Payment(models.Model):
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.membership.member.username} - ${self.amount} - {self.payment_date}" 

@receiver(pre_save, sender=Payment)
def validate_user_type(sender, instance, **kwargs):
        if instance.amount < 0:
            raise ValidationError("Amount must be positive")
        if not Membership.objects.filter(pk=instance.membership_id).exists():
            raise Membership.DoesNotExist("Invalid membership ID")

        
class Attendance(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    branch = models.CharField(max_length=255, default="Dokki")  # Assuming you store location as a string for simplicity

    class Meta:
        unique_together = ['member', 'date']  # Ensures only one attendance record per member per day

    def __str__(self):
        return f"{self.member.get_full_name()} - {self.date}"
