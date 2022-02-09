# Generated by Django 3.1.2 on 2021-01-23 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_listing_previous'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='previous',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='previous', to='auctions.bid'),
        ),
    ]