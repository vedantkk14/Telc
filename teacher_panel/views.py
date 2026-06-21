from django.shortcuts import render
from accounts.decorators import teacher_required

@teacher_required
def teacher_dashboard(request):

    return render(request, 'teachers/teacher_dashboard.html')
