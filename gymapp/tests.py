from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import User, Class, Membership, Payment, Attendance
from datetime import datetime, timedelta

class UserModelTestCase(TestCase):
    def setUp(self):
        # Create a test user for each user type
        self.trainer_user = User.objects.create_user(username='trainer1', user_type=User.TRAINER)
        self.customer_user = User.objects.create_user(username='customer1', user_type=User.CUSTOMER)
        self.member_user = User.objects.create_user(username='member1', user_type=User.MEMBER)

    def test_user_creation(self):
        """Test that users are created with correct attributes"""
        # Check Trainer user
        self.assertEqual(self.trainer_user.username, 'trainer1')
        self.assertEqual(self.trainer_user.user_type, User.TRAINER)

        # Check Customer user
        self.assertEqual(self.customer_user.username, 'customer1')
        self.assertEqual(self.customer_user.user_type, User.CUSTOMER)

        # Check Member user
        self.assertEqual(self.member_user.username, 'member1')
        self.assertEqual(self.member_user.user_type, User.MEMBER)

    def test_user_str_method(self):
        """Test the __str__ method of the User model"""
        # Check the string representation of each user
        self.assertEqual(str(self.trainer_user), 'trainer1')
        self.assertEqual(str(self.customer_user), 'customer1')
        self.assertEqual(str(self.member_user), 'member1')

    def test_default_user_type(self):
        """Test that the default user type is set correctly"""
        # Create a user without specifying user type
        default_user = User.objects.create_user(username='default_user')
        # Check that the default user type is 'Customer'
        self.assertEqual(default_user.user_type, User.CUSTOMER)

    def test_invalid_user_type(self):
        """Test that an error is raised for invalid user type"""
        # Try to create a user with an invalid user type
        with self.assertRaises(ValueError):
            invalid_user = User.objects.create_user(username='invalid_user', user_type='INVALID')
    
    def test_user_type_choices(self):
        """Test that user type choices are limited to the specified options"""
        # Get choices for user type field
        choices = dict(User.USER_TYPE_CHOICES)
        # Check that user type choices match the defined choices
        self.assertEqual(choices, {'TR': 'Trainer', 'CU': 'Customer', 'ME': 'Member'})



class ClassModelTestCase(TestCase):
    def setUp(self):
        # Create a trainer user with user_type='TRAINER'
        self.trainer = User.objects.create_user(username='trainer1', user_type=User.TRAINER)
        start_date = datetime.now()
        self.expected_end_date = start_date + timedelta(days=5)
        
    def test_trainer_assigned_to_class(self):
        """Test that only trainers can be assigned to classes"""
        # Create a class instance with a valid trainer
        class_instance = Class.objects.create(name='Yoga Class', trainer=self.trainer, end_time=self.expected_end_date, description='Relaxing yoga session')
        self.assertEqual(class_instance.trainer, self.trainer)

    def test_non_trainer_assigned_to_class(self):
        """Test that non-trainers cannot be assigned to classes"""
        # Create a user with a user_type other than 'TRAINER'
        non_trainer = User.objects.create_user(username='non_trainer', user_type=User.CUSTOMER)

        # Attempt to create a class instance with a non-trainer user
        with self.assertRaises(ValueError):
            class_instance = Class.objects.create(name='Yoga Class', trainer=non_trainer, description='Relaxing yoga session', end_time=self.expected_end_date)


class MembershipModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password', user_type=User.MEMBER)

    def test_membership_creation_basic(self):
        """Basic test for creating a membership"""
        membership = Membership.objects.create(member=self.user, duration=30, start_date=datetime.now())
        self.assertIsInstance(membership, Membership)

    def test_membership_str_method_basic(self):
        """Basic test for __str__ method of Membership model"""
        membership = Membership.objects.create(member=self.user, duration=30, start_date=datetime.now())
        self.assertEqual(str(membership), f"testuser - 30")

    def test_membership_creation_extensive(self):
        """Extensive test for creating a membership"""
        # Create memberships with different durations and start dates
        start_date_1 = datetime.now()
        membership_1 = Membership.objects.create(member=self.user, duration=30, start_date=start_date_1)

        start_date_2 = datetime.now() - timedelta(days=10)
        membership_2 = Membership.objects.create(member=self.user, duration=90, start_date=start_date_2)

        # Verify memberships were created successfully
        self.assertIsInstance(membership_1, Membership)
        self.assertIsInstance(membership_2, Membership)

        # Verify memberships have different start dates
        self.assertNotEqual(membership_1.start_date, membership_2.start_date)

    def test_membership_valid_date_calculation_extensive(self):
        """Extensive test for membership valid date calculation"""
        # Create a membership with start date and duration
        start_date = datetime.now()
        duration = 30
        membership = Membership.objects.create(member=self.user, duration=duration, start_date=start_date)

        # Calculate the expected end date based on start date and duration
        expected_end_date = start_date + timedelta(days=duration)

        # Verify the membership's end date matches the expected end date
        self.assertEqual(membership.end_date, expected_end_date)


    def test_non_member_assigned_to_membership(self):
        """Test that non-trainers cannot be assigned to classes"""
        # Create a user with a user_type other than 'TRAINER'
        non_member = User.objects.create_user(username='non_member', user_type=User.CUSTOMER)

        # Attempt to create a class instance with a non-trainer user
        with self.assertRaises(ValueError):
            start_date = datetime.now()
            duration = 30
            membership = Membership.objects.create(member=non_member, duration=duration, start_date=start_date)
            

from django.core.exceptions import ValidationError
class PaymentModelTestCase(TestCase):
    def setUp(self):
        # Create a user and a membership for testing
        self.user = User.objects.create_user(username='testuser', password='password', user_type=User.MEMBER)
        start_date = datetime.now()
        duration = 30
        self.membership = Membership.objects.create(member=self.user, duration=duration, start_date=start_date)

    def test_payment_creation(self):
        """Test for creating a payment"""
        payment = Payment.objects.create(membership=self.membership, amount=50.00)
        self.assertIsInstance(payment, Payment)

    def test_payment_str_method(self):
        """Test for __str__ method of Payment model"""
        payment = Payment.objects.create(membership=self.membership, amount=50.00)
        self.assertEqual(str(payment), f"testuser - $50.0 - {payment.payment_date}")

    def test_payment_creation_invalid_membership(self):
        """Test for creating a payment with an invalid membership"""
        # Attempt to create a payment with a non-existent membership
        with self.assertRaises(Membership.DoesNotExist):
            Payment.objects.create(membership_id=9999, amount=50.00)

    def test_payment_amount_negative(self):
        """Test for creating a payment with a negative amount"""
        # Attempt to create a payment with a negative amount
        with self.assertRaises(ValidationError):
            Payment.objects.create(membership=self.membership, amount=-50.00)

    

class AttendanceModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password', user_type=User.MEMBER)

    def test_attendance_creation(self):
        """Test for creating an attendance"""
        # Create an attendance record
        attendance = Attendance.objects.create(member=self.user, date=datetime.now())
        self.assertIsInstance(attendance, Attendance)

    def test_attendance_str_method(self):
        """Test for __str__ method of Attendance model"""
        # Create an attendance record
        attendance = Attendance.objects.create(member=self.user, date=datetime.now())
        self.assertEqual(str(attendance), f"{self.user.get_full_name()} - {attendance.date}")

    def test_attendance_unique_together_constraint(self):
        """Test for unique_together constraint"""
        # Create an attendance record
        attendance_1 = Attendance.objects.create(member=self.user, date=datetime.now(), branch='Dokki')
        
        # Attempt to create another attendance record for the same user and date
        with self.assertRaises(Exception):
            attendance_2 = Attendance.objects.create(member=self.user, date=datetime.now(), branch='Giza')

    # Add more test cases as needed
