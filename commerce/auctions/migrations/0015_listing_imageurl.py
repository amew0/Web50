# Generated by Django 3.1.2 on 2021-02-04 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='imageUrl',
            field=models.URLField(null=True),
        ),
    ]
