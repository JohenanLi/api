# Generated by Django 2.2.4 on 2020-07-09 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='token',
            field=models.CharField(default='0', max_length=200),
        ),
    ]
