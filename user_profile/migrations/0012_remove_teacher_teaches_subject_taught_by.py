# Generated by Django 4.0.3 on 2022-03-10 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0011_alter_teacher_works_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='teaches',
        ),
        migrations.AddField(
            model_name='subject',
            name='taught_by',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='user_profile.teacher'),
        ),
    ]