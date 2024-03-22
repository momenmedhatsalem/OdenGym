# Generated by Django 3.2.10 on 2024-02-15 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='valid_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='instagram',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='duration',
            field=models.IntegerField(choices=[(30, 'Monthly'), (90, '3 Months'), (180, '6 Months'), (365, 'Yearly')]),
        ),
        migrations.AlterField(
            model_name='membership',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
