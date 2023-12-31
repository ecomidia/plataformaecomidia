# Generated by Django 3.2.19 on 2023-05-31 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0002_auto_20230531_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='status',
            name='entities',
            field=models.ManyToManyField(related_name='entities', to='twitter.Entity'),
        ),
    ]
