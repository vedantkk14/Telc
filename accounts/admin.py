from django.contrib import admin
from .models import User, AdminProfile, TeacherProfile, Student


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "role",
        "is_active",
        "is_staff",
        "date_joined",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "full_name",
        "email",
    )

    ordering = ("-date_joined",)

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "department",
        "designation",
    )

    search_fields = (
        "user__full_name",
        "user__email",
        "department",
    )

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "experience_years",
        "specialization"
    )

    search_fields = (
        "user__full_name",
        "user__email",
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "full_name",
        "email",
        "phone_number",
        "exam_batch",
        "date_of_birth",
        "gender",
    )

    search_fields = (
        "full_name",
        "user__email",
        "student_id",
        "phone_number",
        "exam_batch",
    )