# Generated by Django 4.0.3 on 2022-04-08 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]