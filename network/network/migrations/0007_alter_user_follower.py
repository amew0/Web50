# Generated by Django 3.2.6 on 2021-09-17 15:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_user_follower'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='follower',
            field=models.ManyToManyField(related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]