from django.contrib.auth.models import Group

def check_student_group(request):
    if request.user.is_authenticated:
        return {'is_student': request.user.groups.filter(name='Students').exists()}
    return {'is_student': False}

def check_instructor_group(request):
    if request.user.is_authenticated:
        return {'is_instructor': request.user.groups.filter(name='Instructor').exists()}
    return {'is_instructor': False}