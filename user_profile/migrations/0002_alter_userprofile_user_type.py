# Generated by Django 4.0.3 on 2022-03-08 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher')], max_length=10),
        ),
    ]