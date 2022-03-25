from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import *

from datetime import date
from dateutil.relativedelta import relativedelta

class UserSignUpForm(forms.Form):
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)
	email = forms.EmailField()
	username = forms.CharField(max_length=30)
	password = forms.CharField(label = "Passpharse", widget=forms.PasswordInput)
	confirm_password = forms.CharField(label = "Confirm Passpharse",  widget=forms.PasswordInput)
	user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE)

	def clean_username(self):
		username = self.cleaned_data['username']
		if not username.islower():
			raise ValidationError("Keep Username in all lower alphabets.")
		user = User.objects.filter(username=username)
		if user.exists():
			raise ValidationError("Username already exits. Try new one!!!")
		return username

	def clean(self):
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')

		if password != confirm_password:
			msg = "Passwords do not match!!!"
			raise ValidationError(msg)


class UserSignInForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(widget = forms.PasswordInput)

	def clean_username(self):
		#cleaned_data = super().clean()
		username = self.cleaned_data.get('username')
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			raise ValidationError("Username don't exist!!!")
		else:
			return username
			
	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if username:
			user = authenticate(username=username, password=password)
			if user is None:
				raise ValidationError("Password is incorrect!!!")

class UserProfileForm(forms.Form):
	first_name = forms.CharField(max_length=20, disabled=True)
	last_name = forms.CharField(max_length=20, disabled=True)
	email = forms.EmailField(disabled=True)
	username = forms.CharField(max_length=30, disabled=True)
	user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE, disabled=True)
	phone_number = forms.CharField(max_length=10)
	dob = forms.DateField(widget=forms.DateInput)
	address = forms.CharField(max_length=100)

	def clean_phone_number(self):
		phone_number = self.cleaned_data.get('phone_number')
		
		if len(phone_number) != 10 and phone_number.isdigit():
			raise ValidationError("Phone number must have 10 digits only.")
		
		else:
			return phone_number

	def clean_dob(self):
		dob = self.cleaned_data['dob']

		if (dob > (date.today()-relativedelta(years=16))):
			raise ValidationError("Minimum age must be 16 years.")
		else:
			return dob

class CourseApplyForm(forms.Form):
	course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Select Course")
	start_year = forms.CharField(max_length=4)
	
	def __init__(self, *args, **kwargs):
		user_profile = kwargs.pop('user_profile', None)
		super(CourseApplyForm, self).__init__(*args, **kwargs)
		if user_profile is not None:
			if False in user_profile.student.courses.values_list('is_vocational', flat=True):
				self.fields['course'].queryset = Course.objects.filter(is_vocational=True, pre_requisite=user_profile.student.qualification).exclude(id__in=user_profile.student.courses.values_list('id',flat=True))
			else:
				self.fields['course'].queryset = Course.objects.filter(pre_requisite=user_profile.student.qualification).exclude(id__in=user_profile.student.courses.values_list('id',flat=True))

	def clean_start_year(self):
		start_year = self.cleaned_data['start_year']
		if start_year.isdigit() and int(start_year) > 2000:
			return start_year
		else:
			raise ValidationError("Start year must be all digit and after 2000.")

class AddCourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = '__all__'
		widgets = {
		'subjects' : forms.CheckboxSelectMultiple()
		}

	def clean_name(self):
		name = self.cleaned_data['name']
		try:
			Course.objects.get(name__iexact=name)
		except:
			return name
		else:
			raise ValidationError("Course already exits!!!")

class AddSubjectForm(forms.ModelForm):
	name = forms.CharField(max_length=30, label="Subject Name")
	class Meta:
		model = Subject
		exclude = ['teacher']

	def clean_name(self):
		name = self.cleaned_data['name']
		subject = Subject.objects.filter(name__iexact=name)
		if subject.exists():
			raise ValidationError("Subject already registered!!!")
		else:
			return name.lower()

class SearchForm(forms.Form):
	SORT_BY = (
		('Name', (
			('asc_name', "Acesending"),
			('desc_name', 'Descending')
			)),
		('Start_year', (
			('asc_year', "Acesending"),
			('desc_year', 'Descending')
			)),
	)
	name = forms.CharField(label='Search by name',required=False, widget=forms.TextInput(attrs={'placeholder': "Name"}))
	sort_by = forms.ChoiceField(label="Sort by", required=False, choices=SORT_BY)

class AddStudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ['qualification',]

class ChangePasswordForm(forms.Form):
	password = forms.CharField(label = "Passpharse", widget=forms.PasswordInput)
	new_password = forms.CharField(label = "New Passpharse", widget=forms.PasswordInput)
	confirm_password = forms.CharField(label = "Confirm Passpharse",  widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		self.user = user
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

	def clean_password(self):
		password = self.cleaned_data.get('password')
		user = authenticate(username=self.user.username, password=password)
		if user is None:
			msg = "Incorrect Current passphrase!!!"
			raise ValidationError(msg)
		else:
			return password
	def clean(self):
		password = self.cleaned_data.get('password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')

		if password:			
			if password == new_password:
				msg = "Can't use old password!!!"
				raise ValidationError(msg)

			if password != confirm_password:
				msg = "Passwords do not match!!!"
				raise ValidationError(msg)

class ResetPasswordForm(forms.Form):
	email = forms.EmailField(label='Email')

	def clean_email(self):
		email = self.cleaned_data.get('email')
		users = User.objects.filter(email=email)
		if not users.exists():
			msg = "No user with this email!!!"
			raise ValidationError(msg)
		else:
			return email

class ResetPasswordConfirmForm(forms.Form):
	new_password = forms.CharField(label = "New Passpharse", widget=forms.PasswordInput)
	confirm_password = forms.CharField(label = "Confirm Passpharse",  widget=forms.PasswordInput)

	def clean(self):
		password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')

		if password != confirm_password:
			msg = "Passwords do not match!!!"
			raise ValidationError(msg)