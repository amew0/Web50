# Generated by Django 3.1.2 on 2021-01-17 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='listingC',
            field=models.OneToOneField(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='listingC', to='auctions.listing'),
            preserve_default=False,
        ),
    ]
