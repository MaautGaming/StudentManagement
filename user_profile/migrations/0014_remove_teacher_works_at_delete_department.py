# Generated by Django 4.0.3 on 2022-03-11 04:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0013_alter_subject_taught_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='works_at',
        ),
        migrations.DeleteModel(
            name='Department',
        ),
    ]