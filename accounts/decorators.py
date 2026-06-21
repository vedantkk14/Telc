from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):

    decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.role == "ADMIN" or u.is_superuser)
    )
    return decorator(view_func)


def teacher_required(view_func):

    decorator = user_passes_test(
        lambda u: u.is_authenticated and u.role == "TEACHER"
    )
    return decorator(view_func)