from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as rest_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import routers

from . import views

app_name="user_profile"

urlpatterns = [
	path('', views.index, name='dashboard'),
	path('course/delete/<int:pk>', views.delete_course, name='delete_course'),
	path('course/<int:pk>', views.course_details, name='course_details'),
	path('course/', views.courses, name='courses'),
	path('subject/<int:pk>', views.delete_subject, name='delete_subject'),
	path('subject/', views.subjects, name='subjects'),
	path('course/apply/', views.course_apply, name='course_apply'),
	path('students/', views.students, name='students'),
	path('course/students/<int:pk>/', views.course_students, name='course_students'),
	#path('password/change', auth_views.PasswordChangeView.as_view(success_url='/signin/'), name='change_password'),
	path('password/change/', views.change_password, name='change_password'),
	path('password/reset/', views.reset_password, name='password_reset'),

	#path('password/reset/', auth_views.PasswordResetView.as_view(email_template_name='user_profile/password_reset_email.html', success_url='/password/reset/done/'), name='password_reset'),
	path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
	path('password/reset/done/', views.reset_password_done, name='reset_password_done'),
	#path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/password/reset/complete'), name='password_reset_confirm'),
	path('password/reset/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),


	path('signup/', views.sign_up, name='sign_up'),
	path('signin/', views.sign_in, name='sign_in'),
	path('signout/', views.sign_out, name='sign_out'),
	path('api/', views.api_view, name='api_view'),

	path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
	path('api-token-auth/', rest_view.obtain_auth_token),

	path('api/teachers/', views.TeacherList.as_view() , name='teacher-list' ),
	path('api/students/', views.student_list , name='student-list' ),
	path('stu/', views.stu, name='stu')

]