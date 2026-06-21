from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import AdminProfile

User = get_user_model()

class AdminCreationTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create an admin user to perform the creation
        self.admin_user = User.objects.create_user(
            username="mainadmin@test.com",
            email="mainadmin@test.com",
            password="adminpassword123",
            role="ADMIN",
            full_name="Main Admin"
        )
        self.client.login(email="mainadmin@test.com", password="adminpassword123")

    def test_create_admin_success_with_optional_fields(self):
        url = reverse('create_admin')
        data = {
            'full_name': 'New Admin User',
            'email': 'newadmin@test.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
            'department': 'Engineering',
            'designation': 'Senior System Admin'
        }
        # Simulate AJAX request to test the JSON response path
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'success')
        
        # Verify user was created
        user_exists = User.objects.filter(email='newadmin@test.com').exists()
        self.assertTrue(user_exists)
        
        new_user = User.objects.get(email='newadmin@test.com')
        self.assertEqual(new_user.full_name, 'New Admin User')
        
        # Verify profile was created with the correct optional fields
        profile = AdminProfile.objects.get(user=new_user)
        self.assertEqual(profile.department, 'Engineering')
        self.assertEqual(profile.designation, 'Senior System Admin')

    def test_create_admin_success_without_optional_fields(self):
        url = reverse('create_admin')
        data = {
            'full_name': 'Optional Admin User',
            'email': 'optionaladmin@test.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
            'department': '',
            'designation': ''
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'success')
        
        # Verify user and profile exist
        new_user = User.objects.get(email='optionaladmin@test.com')
        profile = AdminProfile.objects.get(user=new_user)
        self.assertIsNone(profile.department)
        self.assertIsNone(profile.designation)

    def test_create_admin_missing_compulsory_fields(self):
        url = reverse('create_admin')
        data = {
            'full_name': '',  # Compulsory
            'email': 'missing@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'department': 'Engineering',
            'designation': 'Lead'
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'error')
        self.assertIn('compulsory fields are required', response_json['messages'][0])
        
        self.assertFalse(User.objects.filter(email='missing@test.com').exists())

    def test_create_admin_passwords_mismatch(self):
        url = reverse('create_admin')
        data = {
            'full_name': 'Mismatch User',
            'email': 'mismatch@test.com',
            'password': 'password123',
            'confirm_password': 'differentpassword',
            'department': 'Engineering',
            'designation': 'Lead'
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'error')
        self.assertIn('Passwords do not match', response_json['messages'][0])
        
        self.assertFalse(User.objects.filter(email='mismatch@test.com').exists())

    def test_create_admin_as_superuser_who_is_not_admin_role(self):
        # Create a superuser whose role is empty
        superuser = User.objects.create_superuser(
            username="superuser@test.com",
            email="superuser@test.com",
            password="superpassword123",
            role=""
        )
        self.client.login(email="superuser@test.com", password="superpassword123")
        url = reverse('create_admin')
        # Check GET request resolves successfully
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TeacherCreationTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create an admin user to perform the creation
        self.admin_user = User.objects.create_user(
            username="mainadmin@test.com",
            email="mainadmin@test.com",
            password="adminpassword123",
            role="ADMIN",
            full_name="Main Admin"
        )
        self.client.login(email="mainadmin@test.com", password="adminpassword123")

    def test_create_teacher_success_with_optional_fields(self):
        url = reverse('create_teacher')
        data = {
            'full_name': 'New Teacher',
            'email': 'newteacher@test.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
            'specialization': 'Mathematics',
            'experience_years': '5'
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'success')
        
        # Verify user and profile exist
        new_user = User.objects.get(email='newteacher@test.com')
        self.assertEqual(new_user.role, 'TEACHER')
        
        from accounts.models import TeacherProfile
        profile = TeacherProfile.objects.get(user=new_user)
        self.assertEqual(profile.specialization, 'Mathematics')
        self.assertEqual(profile.experience_years, 5)

    def test_create_teacher_success_without_optional_fields(self):
        url = reverse('create_teacher')
        data = {
            'full_name': 'New Teacher 2',
            'email': 'newteacher2@test.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
            'specialization': 'German',
            'experience_years': ''
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'success')
        
        new_user = User.objects.get(email='newteacher2@test.com')
        from accounts.models import TeacherProfile
        profile = TeacherProfile.objects.get(user=new_user)
        self.assertEqual(profile.specialization, 'German')
        self.assertIsNone(profile.experience_years)

    def test_create_teacher_missing_compulsory_fields(self):
        url = reverse('create_teacher')
        # Missing specialization (which is compulsory)
        data = {
            'full_name': 'New Teacher 3',
            'email': 'newteacher3@test.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
            'specialization': '',
            'experience_years': '2'
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'error')
        self.assertIn('compulsory fields are required', response_json['messages'][0])
        
        self.assertFalse(User.objects.filter(email='newteacher3@test.com').exists())


class StudentCreationTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create an admin user to perform the creation
        self.admin_user = User.objects.create_user(
            username="mainadmin@test.com",
            email="mainadmin@test.com",
            password="adminpassword123",
            role="ADMIN",
            full_name="Main Admin"
        )
        self.client.login(email="mainadmin@test.com", password="adminpassword123")

    def test_create_student_success_with_optional_fields(self):
        url = reverse('create_student')
        data = {
            'student_id': 'STU-999',
            'full_name': 'New Student',
            'email': 'student@test.com',
            'phone_number': '1234567890',
            'exam_batch': 'B2',
            'date_of_birth': '2000-01-01',
            'gender': 'MALE'
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'success')
        
        # Verify student exists in Student table
        from accounts.models import Student
        student_exists = Student.objects.filter(student_id='STU-999').exists()
        self.assertTrue(student_exists)
        
        student = Student.objects.get(student_id='STU-999')
        self.assertEqual(student.full_name, 'New Student')
        self.assertEqual(student.email, 'student@test.com')
        self.assertEqual(student.phone_number, '1234567890')
        self.assertEqual(student.exam_batch, 'B2')
        self.assertEqual(str(student.date_of_birth), '2000-01-01')
        self.assertEqual(student.gender, 'MALE')

    def test_create_student_success_without_optional_fields(self):
        url = reverse('create_student')
        data = {
            'student_id': 'STU-888',
            'full_name': 'New Student 2',
            'email': 'student2@test.com',
            'phone_number': '9876543210',
            'exam_batch': 'A1',
            'date_of_birth': '',
            'gender': ''
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'success')
        
        from accounts.models import Student
        student = Student.objects.get(student_id='STU-888')
        self.assertIsNone(student.date_of_birth)
        self.assertIsNone(student.gender)

    def test_create_student_missing_compulsory_fields(self):
        url = reverse('create_student')
        data = {
            'student_id': '',  # missing
            'full_name': 'New Student 3',
            'email': 'student3@test.com',
            'phone_number': '1111111111',
            'exam_batch': 'C1',
            'date_of_birth': '',
            'gender': ''
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'error')
        self.assertIn('compulsory fields are required', response_json['messages'][0])
        
        from accounts.models import Student
        self.assertFalse(Student.objects.filter(email='student3@test.com').exists())


class LogoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@test.com",
            email="testuser@test.com",
            password="testpassword123",
            role="TEACHER",
            full_name="Test User"
        )

    def test_logout_redirects_and_clears_session(self):
        # Log in
        self.client.login(email="testuser@test.com", password="testpassword123")
        
        # Verify authenticated user is NOT automatically redirected when visiting login page
        response = self.client.get(reverse('login_page'))
        self.assertEqual(response.status_code, 200)
        
        # Log out
        logout_response = self.client.get(reverse('logout'))
        self.assertEqual(logout_response.status_code, 302)
        self.assertRedirects(logout_response, reverse('login_page'))
        
        # Verify no longer authenticated / no redirect
        response_after = self.client.get(reverse('login_page'))
        self.assertEqual(response_after.status_code, 200)

    def test_login_post_success_admin(self):
        # Create an admin user
        admin_user = User.objects.create_user(
            username="adminuser@test.com",
            email="adminuser@test.com",
            password="adminpassword123",
            role="ADMIN",
            full_name="Admin Name"
        )
        url = reverse('login_page')
        data = {
            'email': 'adminuser@test.com',
            'password': 'adminpassword123',
            'remember_me': ''
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('welcome_message', response.context)
        self.assertEqual(response.context['welcome_message'], "Welcome Admin Name. Redirecting to dashboard...")
        self.assertEqual(response.context['redirect_url'], reverse('admin_dashboard'))

    def test_login_post_success_teacher(self):
        url = reverse('login_page')
        data = {
            'email': 'testuser@test.com',
            'password': 'testpassword123',
            'remember_me': ''
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('welcome_message', response.context)
        self.assertEqual(response.context['welcome_message'], "Welcome Test User. Redirecting to dashboard...")
        self.assertEqual(response.context['redirect_url'], reverse('teacher_dashboard'))


