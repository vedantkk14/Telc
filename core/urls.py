"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from admin_panel.views import admin_reports
from django.contrib import admin
from django.urls import path

from accounts.views import *
from admin_panel.views import *
from teacher_panel.views import *

urlpatterns = [
    path("admin/", admin.site.urls),

    #auth routes
    path(route="", view=login_page, name="login_page"),
    path(route="logout/", view=logout_view, name="logout"),

    #admin side routes
    path(route="admin_dashboard/", view=admin_dashboard, name="admin_dashboard"),
    path(route="create_admin/", view=create_admin, name="create_admin"),
    path(route="create_teacher/", view=create_teacher, name="create_teacher"),
    path(route="create_student/", view=create_student, name="create_student"),
    path(route="admin_student_management/", view=admin_student_management, name="admin_student_management"),
    path(route="admin_teacher_management/", view=admin_teacher_management, name="admin_teacher_management"),
    path(route="admin_examinations/", view=admin_examinations, name="admin_examinations"),
    path(route="admin_questionbank/", view=admin_questionbank, name="admin_questionbank"),
    path(route="admin_display_results/", view=admin_display_results, name="admin_display_results"),
    path(route="admin_reports/", view=admin_reports, name="admin_reports"),
    path(route="admin_notifications/", view=admin_notifications, name="admin_notifications"),
    
    #teacher side routes
    path(route="teacher_dashboard/", view=teacher_dashboard, name="teacher_dashboard"),
    path(route="teacher_questionbank/", view=teacher_questionbank, name="teacher_questionbank"),
    path(route="teacher_exams/", view=teacher_exams, name="teacher_exams"),
    path(route="teacher_evaluations/", view=teacher_evaluations, name="teacher_evaluations"),
    path(route="teacher_performance_eval/", view=teacher_performance_eval, name="teacher_performance_eval"),
    path(route="teacher_messages/", view=teacher_messages, name="teacher_messages"),
]

