# Generated by Django 4.0.3 on 2022-03-10 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_department_teacher_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(null=True, to='user_profile.course'),
        ),
    ]
