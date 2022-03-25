from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse as res

from .serializers import *
from .decorators import *
from .models import *
from .forms import *

@api_view(['GET'])
def student_list(request):
	if request.method == 'GET':
		students = Student.objects.all()
		serializer = StudentSerializer(students, many=True)
		return JsonResponse(serializer.data, safe=False)


class TeacherList(generics.ListAPIView):
	queryset = Teacher.objects.all()
	serializer_class = TeacherSerializer

	def get(self, request, *args, **kwargs):
		self.queryset = self.get_queryset()
		return Response({'teachers': self.queryset}, template_name='user_profile/teacher_api.html')

@api_view(['GET'])
def stu(request):
	students = Student.objects.all()
	serializer = StudentSerializer(students, many=True)
	print(serializer)
	return Response({"students": serializer.data}, template_name='user_profile/student_api.html')


def sign_up(request):
	if request.method == "POST":
		form = UserSignUpForm(request.POST)
		if form.is_valid():
			clean_data = form.cleaned_data
			first_name = clean_data['first_name'].lower()
			last_name = clean_data['last_name'].lower()
			email = clean_data['email']
			username = clean_data['username']
			password = clean_data['password']
			user_type = clean_data['user_type']
			
			user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
			UserProfile.objects.create(user=user, user_type=user_type)

			messages.success(request, 'User Created Successfully!!!')
			return redirect(reverse('user_profile:sign_in'))
	else:
		form = UserSignUpForm()
	return render(request, 'user_profile/sign_up.html', {'form': form })

def sign_in(request):
	if request.user.is_authenticated:
		return redirect(reverse('user_profile:dashboard'))

	if request.method == "POST":
		form = UserSignInForm(request.POST)
		if form.is_valid():
			clean_data = form.cleaned_data
			username = clean_data['username']
			password = clean_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect(reverse('user_profile:dashboard'))
	else:
		form = UserSignInForm()
	return render(request, 'user_profile/sign_in.html', {'form': form})

def sign_out(request):
	logout(request)
	return redirect(reverse("user_profile:sign_in"))

@login_required(login_url='/signin')
def index(request):
	user_profile = request.user.userprofile
	initial = {
		'first_name': user_profile.user.first_name.title(),
		'last_name': user_profile.user.last_name.title(),
		'username': user_profile.user.username,
		'email': user_profile.user.email,
		'user_type': user_profile.user_type,
		'phone_number': user_profile.phone_number,
		'dob': user_profile.dob,
		'address': user_profile.address,
		}
	context = {}
	if request.method == "POST":
		if 'user_profile' in request.POST:
			form = UserProfileForm(request.POST, initial=initial, prefix='user_profile')
			context['form'] = form
			if form.is_valid() and form.has_changed():
				print("Changing form")
				clean_data = form.cleaned_data
				phone_number = clean_data['phone_number']
				dob = clean_data['dob']
				address = clean_data['address']

				UserProfile.objects.filter(user=request.user).update(phone_number=phone_number, dob=dob, address=address)
				messages.success(request, 'Profile updated successfully!!!')
				return redirect(reverse('user_profile:dashboard'))

		elif 'student' in request.POST:
			student = Student.objects.filter(user_profile__user__username=request.user.username)
			if student.exists():
				studentform = AddStudentForm(request.POST ,initial={'qualification':request.user.userprofile.student.qualification}, prefix='student')
				context['studentform'] = studentform
			else:
				studentform = AddStudentForm(request.POST, prefix='student')
				context['studentform'] = studentform
			if studentform.is_valid() and studentform.has_changed():
				qualification = studentform.cleaned_data.get('qualification')
				student = Student.objects.get_or_create(user_profile=request.user.userprofile)
				student[0].qualification = qualification
				student[0].save()
				messages.success(request, 'Profile updated successfully!!!')
				return redirect(reverse('user_profile:dashboard'))
	else:
		context['form'] = UserProfileForm(initial=initial, prefix='user_profile')
	if request.user.userprofile.user_type == 'student':
		student = Student.objects.filter(user_profile=request.user.userprofile)
		if student.exists():
			context['studentform'] = AddStudentForm(initial={'qualification':request.user.userprofile.student.qualification}, prefix='student')
		else:
			context['studentform'] = AddStudentForm(prefix='student')
	return render(request, 'user_profile/dashboard.html', context)

@login_required(login_url='/signin/')
def courses(request):
	if request.method == "POST":
		form = AddCourseForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Course added successfully!!!')
			return redirect(reverse('user_profile:courses'))
	
	else:
		courses = Course.objects.all()
		context = {'courses': courses}
		user_profile = request.user.userprofile
		if user_profile.user_type != "teacher":
			message = "You don't have previledge to add course."
			return render(request, 'user_profile/courses.html', {'message': message})
		
		else:
			form = AddCourseForm()
		context['form'] = form
		return render(request, 'user_profile/courses.html', context)

@login_required(login_url='/signin/')
def course_details(request, pk):
	course = Course.objects.get(pk=pk)
	return render(request, 'user_profile/course_details.html', {'course': course})


@login_required(login_url='/signin/')
@check_allowed_user_role('student')
def course_apply(request):
	if request.user.userprofile.user_type == "teacher":
		return redirect(reverse('user_profile:dashboard'))
	initial = {
		"start_year": request.user.userprofile.student.start_year
	}
	if request.method == "POST":
		form = CourseApplyForm(request.POST, initial=initial, **{"user_profile": request.user.userprofile})
		if form.is_valid():
			clean_data = form.cleaned_data
			start_year = clean_data['start_year']
			course = clean_data['course']
			student = Student.objects.get_or_create(user_profile=request.user.userprofile)[0]
			student.start_year = start_year
			student.courses.add(course)
			messages.success(request, 'Applied for course successfully!!!')
			return redirect(reverse('user_profile:dashboard'))
	else:
		form = CourseApplyForm(initial=initial, **{"user_profile": request.user.userprofile})
	courses = request.user.userprofile.student.courses.values()
	return render(request, 'user_profile/course_apply.html', {"form": form, 'courses': courses})

@login_required(login_url='/signin/')
def course_students(request, pk):
	form = SearchForm(request.GET)
	search_string = request.GET.get('name', '')
	sort_by = request.GET.get('sort_by', 'asc_name')
	first_name = Q(user_profile__user__first_name__icontains= search_string)
	last_name = Q(user_profile__user__last_name__icontains= search_string)
	students = Student.objects.filter(courses__id=pk).filter( first_name | last_name )

	if sort_by =='desc_year':
		students = students.order_by('-start_year')
	elif sort_by == 'asc_year':
		students = students.order_by('start_year')
	elif sort_by == 'desc_name':
		students = students.order_by(Coalesce('user_profile__user__first_name', 'user_profile__user__last_name').desc())
	else:
		students = students.order_by(Coalesce('user_profile__user__first_name', 'user_profile__user__last_name').asc())
	return render(request, 'user_profile/students.html', {'form':form, 'students': students, 'course_id':pk})


@login_required(login_url='/signin/')
@check_allowed_user_role(role='teacher')
def students(request):
	if request.method == 'GET':
		form = SearchForm(request.GET)
		search_string = request.GET.get('name', '')
		sort_by = request.GET.get('sort_by', 'asc_name')
		first_name = Q(user_profile__user__first_name__icontains = search_string)
		last_name = Q(user_profile__user__last_name__icontains=search_string)
		students = Student.objects.filter( first_name | last_name )

		if sort_by =='desc_year':
			students = students.order_by('-start_year')
		elif sort_by == 'asc_year':
			students = students.order_by('start_year')
		elif sort_by == 'desc_name':
			students = students.order_by(Coalesce('user_profile__user__first_name', 'user_profile__user__last_name').desc())
		else:
			students = students.order_by(Coalesce('user_profile__user__first_name', 'user_profile__user__last_name').asc())

	return render(request, 'user_profile/students.html', {'form':form, 'students': students})

@login_required(login_url='/signin')
@check_allowed_user_role(role='teacher')
def delete_subject(request, pk):
	print(pk)
	#if request.method == "DELETE":
	Subject.objects.filter(pk=pk).delete()
	messages.success(request, "Subject deleted successfully")
	return redirect(reverse('user_profile:subjects'))

@login_required(login_url='/signin/')
def subjects(request):
	SubjectsFormSet = formset_factory(AddSubjectForm, extra=2)
	teacher = request.user.userprofile.teacher
	context = {}
	context['info'] = teacher
	context['subjects'] = Subject.objects.filter(teacher=teacher)
	if request.method == "POST":
		formset = SubjectsFormSet(request.POST, request.FILES)
		if formset.is_valid():
			for form in formset:
				name = form.cleaned_data.get('name')
				if name != None:
					Subject.objects.create(name=name, teacher=teacher)
					messages.success(request, name + ' added successfully to your subjects list!!!')
			return redirect(reverse('user_profile:subjects'))
	else:
		formset = SubjectsFormSet()
	context['formset']= formset
	return render(request, 'user_profile/subjects.html', context)

@login_required(login_url='/signin')
def delete_course(request, pk):
	print(pk)
	Course.objects.filter(pk=pk).delete()
	messages.success(request, "Subject deleted successfully")
	return redirect(reverse('user_profile:courses'))

@login_required(login_url='/signin/')
def change_password(request):
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST, user=request.user)
		if form.is_valid():
			password = form.cleaned_data.get('password')
			new_password = form.cleaned_data.get('new_password')
			user = authenticate(username=request.user.username, password=password)
			if user is None:
				messages.error(request, 'Incorrect passphrase!!!')
			else:
				user.set_password(password)
				user.save
				update_session_auth_hash(request, user)
				messages.success(request, 'Your password was successfully updated!')
				return redirect('user_profile:dashboard')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = ChangePasswordForm()
	return render(request, 'user_profile/change_password.html', {'form': form})

def reset_password(request):
	if request.method == 'POST':
		form = ResetPasswordForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			user = User.objects.get(email=email)
			subject = "Reset Password"
			email_template_name = "user_profile/password_reset_email.txt"
			c = {
			"email":user.email,
			'domain':'127.0.0.1:8000',
			'site_name': 'Website',
			"uid": urlsafe_base64_encode(force_bytes(user.pk)),
			"user": user,
			'token': default_token_generator.make_token(user),
			'protocol': 'http',
			}
			email = render_to_string(email_template_name, c)
			send_mail(subjects, email,'admin@example.com', [user.email], fail_silently=False)
			return redirect(reverse('user_profile:reset_password_done'))
	else:
		form = ResetPasswordForm()
	return render(request, 'user_profile/reset_password.html', context={'form': form})

def reset_password_done(request):
	return render(request, 'user_profile/reset_password_done.html')

def reset_password_confirm(request, uidb64, token):
	uid = force_str(urlsafe_base64_decode(uidb64))
	user = User.objects.get(id=uid)
	if not default_token_generator.check_token(user, token):
		messages.error(request, 'Invalid Url for reseting password!!!')
		return redirect('user_profile:sign_in')
	if request.method == "POST":
		form = ResetPasswordConfirmForm(request.POST)
		if form.is_valid():
			password = form.cleaned_data.get('new_password')
			user = User.objects.get(pk=uid)
			user.set_password(password)
			user.save()
			messages.success(request, 'Password Reset Successfully!!!')
			return redirect('user_profile:sign_in')
	else:
		form = ResetPasswordConfirmForm()
	return render(request, 'user_profile/password_reset_confirm.html', context={'form': form})
