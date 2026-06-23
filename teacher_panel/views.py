from django.shortcuts import render
from accounts.decorators import teacher_required

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
