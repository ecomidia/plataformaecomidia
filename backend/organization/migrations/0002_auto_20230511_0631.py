# Generated by Django 3.2.19 on 2023-05-11 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='facebook_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='instagram_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='twitter_url',
            field=models.URLField(null=True),
        ),
    ]
