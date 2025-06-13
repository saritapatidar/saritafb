from django.test import TestCase
from rest_framework.exceptions import ValidationError
from fb.models import CustomUser, CreatePost, Comment,UserProfile
from fb.serializers import userserializer, postserializer, parentserializer, commentserializer, Loginserializer, registrationserializer


class SerializerTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            firstname="John",
            lastname="Doe",
            email="john@example.com",
            phone_number="8827489151",
            password="Asdf@123",
            Date_of_birth="1990-01-01"
        )
        self.profile=UserProfile.objects.create(user=self.user)
        self.post = CreatePost.objects.create(user=self.profile, content="Test Post")
        self.comment = Comment.objects.create(user=self.user, post=self.post, text="Test Comment")
        self.reply = Comment.objects.create(user=self.user, post=self.post, text="Reply", parent=self.comment)

    def test_user_serializer(self):
        serializer=userserializer(instance=self.user)
        self.assertEqual(serializer.data['firstname'],'John')
        self.assertEqual(serializer.data['phone_number'],'8827489151')
        self.assertEqual(serializer.data['email'],'john@example.com')


    def test_postserializer(self):
        serializer=postserializer(instance=self.post)
        self.assertEqual(serializer.data['user'],"John")
        self.assertEqual(serializer.data['like_count'],0)

    def test_parent_serializer(self):
        serializer = parentserializer(instance=self.comment)
        data = serializer.data
        self.assertEqual(data['user'], "John")


    def test_commentserializer(self):
        serializer=commentserializer(instance=self.comment)
        self.assertEqual(serializer.data['user'],'John')
        self.assertEqual(len(serializer.data['replies']),1)


    def test_loginserializer(self):
        data={'phone_number':'8827489139','password':'Asdf@123'}
        serializer=Loginserializer(data=data)
        self.assertTrue(serializer.is_valid())


    def test_registrationserializer(self):
        data={'firstname':'payal','lastname':'patidar','Date_of_birth':'2000-09-12','email':'payal@gmail.com','phone_number':'9981979655','password':'Asdf@123'}
        serializer=registrationserializer(data=data)
        self.assertTrue(serializer.is_valid(),serializer.errors)
        self.assertEqual(serializer.data['firstname'],"payal")
        self.assertNotEqual(serializer.data['phone_number'],'9981979650')
       
























#     def test_login_serializer_invalid(self):
#         data = {'phone_number': '', 'password': ''}
#         serializer = Loginserializer(data=data)
#         self.assertFalse(serializer.is_valid())

#     def test_registration_serializer_create(self):
#         data = {
#             'firstname': 'Alice',
#             'lastname': 'Smith',
#             'Date_of_birth': '1995-05-15',
#             'gender': 'Female',
#             'email': 'alice@example.com',
#             'phone_number': '9876543210',
#             'password': 'alicepass'
#         }
#         serializer = registrationserializer(data=data)
#         self.assertTrue(serializer.is_valid(), serializer.errors)
#         user = serializer.save()
#         self.assertNotEqual(user.password, 'alicepass')  # Password should be hashed
#         self.assertEqual(user.firstname, 'Alice')
