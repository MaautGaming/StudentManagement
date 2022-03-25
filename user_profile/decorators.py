from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import *


def check_allowed_user_role(role):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			if request.user.userprofile.user_type == role:
				return view_func(request, *args, **kwargs)
			else:
				#messages.error(request, "You are not authorised!!!")
				raise PermissionDenied

		return wrapper_func
	return decorator


# def is_user_teacher(function):
# 	@wraps(function)
# 	def wrap(request, *args, **kwargs):
# 		if request.user.userprofile.user_type == 'teacher':
# 			return function(request, *args, **kwargs)
# 		else:
# 			#messages.error(request, "You are not authorised!!!")
# 			raise PermissionDenied

# 	return wrap