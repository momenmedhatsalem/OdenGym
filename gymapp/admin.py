from django.contrib import admin
from gymapp.models import User, Member, Membership
# Register your models here.
admin.site.register(User)
admin.site.register(Member)
admin.site.register(Membership)