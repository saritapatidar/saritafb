
from django.test import TestCase
from fb.models import CustomUser, CreatePost, UserProfile, FriendRequest, Follow, Comment
from django.core.exceptions import ValidationError
from fb.models import validate_password

class ModelTests(TestCase):

    def setUp(self):
        self.staff_user = CustomUser.objects.create_user(
            phone_number='1234567890',
            email='staff@example.com',
            password='Password@123',
            firstname='Staff',
            lastname='User',
            is_staff=True
        )
        self.super_user = CustomUser.objects.create_user(
            phone_number='0987654321',
            email='super@example.com',
            password='Password@123',
            firstname='Super',
            lastname='User',
            is_superuser=True
        )
        self.normal_user = CustomUser.objects.create_user(
            phone_number='1122334455',
            email='nirmal@example.com',
            password='Password@123',
            firstname='Nirmal',
            lastname='patidar',
            
        )

    def test_user_creation_success(self):
        user = CustomUser.objects.create_user(
            phone_number='1234567893',
            email='test@example.com',
            password='Password@123',
            firstname='Test',
            lastname='User'
        )
        self.assertEqual(user.phone_number, '1234567893')
        self.assertTrue(user.check_password('Password@123'))

    def test_phone_number_validation_invalid(self):
        with self.assertRaises(ValidationError):
            user = CustomUser(
                phone_number='abc123',
                email='fail@example.com',
                password='Password@123'
            )
            user.clean()

    def test_phone_and_password_validation_valid(self):
        user = CustomUser(
            phone_number='1234567890',
            email='valid@example.com',
            password='Password@123'
        )
        try:
            user.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")

    def test_password_validation_too_short(self):
        with self.assertRaises(ValidationError):
            user = CustomUser(
                phone_number='1234567890',
                email='fail@example.com',
                password='Pwd@1'
            )
            user.clean()

    def test_valid_password(self):
        try:
            validate_password("StrongPass1@")
        except ValidationError:
            self.fail("validate_password() raised ValidationError unexpectedly!")

    def test_too_short_password(self):
        with self.assertRaisesMessage(ValidationError, "Password must be at least 8 characters long."):
            validate_password("A1@b")

    def test_missing_uppercase(self):
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one uppercase letter."):
            validate_password("strongpass1@")

    def test_missing_lowercase(self):
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one lowercase letter."):
            validate_password("STRONGPASS1@")

    def test_missing_digit(self):
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one digit."):
            validate_password("StrongPass@")

    def test_missing_special_character(self):
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one special character."):
            validate_password("StrongPass1")

    def test_user_profile_created(self):
        user = CustomUser.objects.create_user(
            phone_number='1234567891',
            email='test@example.com',
            password='Password@123',
            firstname='Test',
            lastname='User'
        )
        profile = UserProfile.objects.create(user=user)
        self.assertEqual(profile.user, user)

    def test_create_post(self):
        profile = UserProfile.objects.create(user=self.normal_user)
        post = CreatePost.objects.create(user=profile, content="My first post")
        self.assertEqual(post.content, "My first post")
        self.assertEqual(post.user, profile)

    def test_like_post(self):
        profile = UserProfile.objects.create(user=self.normal_user)
        post = CreatePost.objects.create(user=profile, content="Like this post")
        post.likes.add(self.staff_user)
        self.assertEqual(post.likes.count(), 1)

    def test_follow_user(self):
        user2 = CustomUser.objects.create_user(
            phone_number='9981979634',
            email='ravina@gmail.com',
            password="Asdf@123",
            firstname='Ravina',
            lastname='Patidar'
        )
        follow = Follow.objects.create(follower=self.normal_user, followed=user2)
        self.assertEqual(follow.follower, self.normal_user)
        self.assertEqual(follow.followed, user2)

    def test_friend_request(self):
        user2 = CustomUser.objects.create_user(
            phone_number='9981979636',
            email='arpita@gmail.com',
            password="Asdf@123",
            firstname='Arpita',
            lastname='Patidar'
        )
        friend_request = FriendRequest.objects.create(from_user=self.normal_user, to_user=user2)
        self.assertEqual(friend_request.from_user, self.normal_user)
        self.assertEqual(friend_request.to_user, user2)

    def test_comment_creation(self):
        profile = UserProfile.objects.create(user=self.normal_user)
        post = CreatePost.objects.create(user=profile, content="Post with comments")
        new_comment = Comment.objects.create(post=post, user=self.staff_user, text="Nice post")
        self.assertEqual(new_comment.text, "Nice post")
        self.assertEqual(new_comment.post, post)

    def test_has_module_perms_for_staff_user(self):
        self.assertTrue(self.staff_user.has_module_perms("any_label"))

    def test_has_module_perms_for_normal_user(self):
        self.assertFalse(self.normal_user.has_module_perms("any_label"))

    def test_has_perm_for_superuser(self):
        self.assertTrue(self.super_user.has_perm("any_permission"))

    def test_has_perm_for_normal_user(self):
        self.assertFalse(self.normal_user.has_perm("any_permission"))
            

