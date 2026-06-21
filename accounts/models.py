from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICE = (
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher')
    )

    full_name = models.CharField(
        max_length=150
    )

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICE
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username", "full_name", "role"]

    def __str__(self):
        return self.email


class AdminProfile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )

    admin_id = models.CharField(
        max_length=10,
        unique=True,
        editable=False
    )

    department = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    designation = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        if not self.admin_id:

            last_admin = AdminProfile.objects.order_by('-id').first()

            if last_admin:
                number = int(last_admin.admin_id[3:]) + 1
            else:
                number = 1

            self.admin_id = f"ADM{number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.designation


class TeacherProfile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )

    teacher_id = models.CharField(
        max_length=10,
        unique=True,
        editable=False
    )

    experience_years = models.PositiveIntegerField(null=True, blank=True)

    specialization = models.CharField(
        max_length=100
    )

    def save(self, *args, **kwargs):

        if not self.teacher_id:

            last_teacher = TeacherProfile.objects.order_by('-id').first()

            if last_teacher:
                number = int(last_teacher.teacher_id[3:]) + 1
            else:
                number = 1

            self.teacher_id = f"TCH{number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.teacher_id


class Student(models.Model):

    EXAM_BATCH_CHOICES = [
        ("A1", "A1"),
        ("A2", "A2"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("C1", "C1"),
        ("C2", "C2")
    ]

    student_id = models.CharField(
        max_length=20,
        unique=True
    )

    full_name = models.CharField(
        max_length=200
    )

    email = models.EmailField(
        unique=True
    )

    phone_number = models.CharField(
        max_length=15
    )

    exam_batch = models.CharField(
        max_length=5,
        choices=EXAM_BATCH_CHOICES
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=20,
        choices=[
            ('MALE', 'Male'),
            ('FEMALE', 'Female'),
            ('OTHER', 'Other')
        ],
        null=True,
        blank=True
    )
    registration_date = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"