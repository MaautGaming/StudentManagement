from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	USER_TYPE = [
    ('student', 'Student'),
    ('teacher', 'Teacher'),
	]
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=10, null=True)
	dob = models.DateField(null=True)
	address = models.CharField(max_length=100, null=True)
	user_type = models.CharField(max_length=10, choices=USER_TYPE)

	def __str__(self):
		return self.user.username

class Course(models.Model):
	QUALIFICATIONS = [
	('higher_secondary', 'Higher Secondary'),
	('graduate', 'Graduate'),
	('post_graduate', 'Post Graduate'),
	]
	name = models.CharField(max_length=50)
	duration = models.IntegerField()
	pre_requisite = models.CharField(max_length=20, choices=QUALIFICATIONS)
	is_vocational = models.BooleanField(default=False)
	subjects = models.ManyToManyField('Subject')

	def __str__(self):
		return self.name

class Subject(models.Model):
	name = models.CharField(max_length=30)
	teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)

	def __str__(self):
		return self.name


class Student(models.Model):
	QUALIFICATIONS = [
	('higher_secondary', 'Higher Secondary'),
	('graduate', 'Graduate'),
	('post_graduate', 'Post Graduate'),
	]
	user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
	qualification = models.CharField(max_length=20, choices=QUALIFICATIONS)
	courses = models.ManyToManyField(Course, null=True, blank=True)
	start_year = models.CharField(max_length=4, null=True, blank=True)

	def __str__(self):
		return self.user_profile.user.username


class Teacher(models.Model):
	user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

	def __str__(self):
		return self.user_profile.user.username