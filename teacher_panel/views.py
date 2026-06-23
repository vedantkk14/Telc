from django.shortcuts import render
from accounts.decorators import teacher_required
from accounts.models import User

@teacher_required
def teacher_dashboard(request):
    return render(request, 'teachers/teacher_dashboard.html')


@teacher_required
def teacher_questionbank(request):
    return render(request, 'teachers/teacher_questionbank.html')


@teacher_required
def teacher_exams(request):
    return render(request, 'teachers/teacher_exams.html')


@teacher_required
def teacher_evaluations(request):
    return render(request, 'teachers/teacher_evaluations.html')


@teacher_required
def teacher_performance_eval(request):
    return render(request, 'teachers/teacher_performance_eval.html')


@teacher_required
def teacher_messages(request):
    admins = User.objects.filter(role='ADMIN')
    return render(request, 'teachers/teacher_messages.html', {
        'admins': admins,
        'active_page': 'messages'
    })

