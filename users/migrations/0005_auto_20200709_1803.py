# Generated by Django 2.2.4 on 2020-07-09 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200709_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='password',
            field=models.CharField(max_length=100, verbose_name='验证码'),
        ),
    ]