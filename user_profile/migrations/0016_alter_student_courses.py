# Generated by Django 4.0.3 on 2022-03-16 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0015_rename_taught_by_subject_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(null=True, to='user_profile.course'),
        ),
    ]