from django.test import TestCase
from fb.models import CustomUser,CreatePost,UserProfile,FriendRequest,Follow,Comment
from django.core.exceptions import ValidationError
 

class ModelTests(TestCase):

    def test_create_user(self):
        self.user = CustomUser.objects.create_user(
            phone_number='1234567890',
            email='test@example.com',
            password='Password@123',
            firstname='Test',
            lastname='User'
        )
        self.profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(self.user,self.user)

    def test_user_creation_success(self):
    	self.user = CustomUser.objects.create_user(phone_number='1234567890',email='test@example.com',password='Password@123',firstname='Test',lastname='User')
    	self.assertEqual(self.user.phone_number,'1234567890')
    	self.assertTrue(self.user.check_password('Password@123'))

    def test_phone_number_validation_invalid(self):
        with self.assertRaises(ValidationError):
            user = CustomUser(
                phone_number='abc123',
                email='fail@example.com',
                password='Password@123'
            )
            user.clean()

    def test_password_validation_too_short(self):
        with self.assertRaises(ValidationError):
            user = CustomUser(
                phone_number='1234567890',
                email='fail@example.com',
                password='Pwd@1'
            )
            user.clean()

    def test_user_profile_created(self):
    	self.user = CustomUser.objects.create_user(phone_number='1234567890',email='test@example.com',password='Password@123',firstname='Test',lastname='User')
    	self.profile = UserProfile.objects.create(user=self.user)
    	self.assertEqual(self.profile.user,self.user)

    def test_create_post(self):
    	self.user = CustomUser.objects.create_user(phone_number='1234567890',email='test@example.com',password='Password@123',firstname='Test',lastname='User')
    	self.profile = UserProfile.objects.create(user=self.user)
    	post = CreatePost.objects.create(user=self.profile, content="My first post")
    	self.assertEqual(post.content, "My first post")
    	self.assertEqual(post.user, self.profile)

    def test_like_post(self):
    	self.user = CustomUser.objects.create_user(phone_number='1234567890',email='test@example.com',password='Password@123',firstname='Test',lastname='User')
    	self.profile = UserProfile.objects.create(user=self.user)
    	post = CreatePost.objects.create(user=self.profile, content="Like this post")
    	post.likes.add(self.user)
    	self.assertEqual(post.likes.count(), 1)

    def test_follow_user(self):
    	self.user = CustomUser.objects.create_user(phone_number='1234567890',email='test@example.com',password='Password@123',firstname='Test',lastname='User')
    	user2=CustomUser.objects.create_user(phone_number='9981979634',email='ravina@gmail.com',password="Asdf@123",firstname='ravina',lastname='patidar')
    	follow=Follow.objects.create(follower=self.user,followed=user2)
    	self.assertEqual(follow.follower,self.user)
    	self.assertEqual(follow.followed,user2)


    def test_friend_request(self):
    	user2=CustomUser.objects.create(phone_number='9981979636',email='Arpita@gmail.com',password="Asdf@123",firstname='Arpita',lastname='patidar')
    	self.user = CustomUser.objects.create_user(phone_number='1234567890',email='test@example.com',password='Password@123',firstname='Test',lastname='User')
    	friend_request=FriendRequest.objects.create(from_user=self.user,to_user=user2)
    	self.assertEqual(friend_request.from_user,self.user)
    	self.assertEqual(friend_request.to_user,user2)
    

    def test_for_comment(self):
    	self.user = CustomUser.objects.create_user(phone_number='1234567890',email='test@example.com',password='Password@123',firstname='Test',lastname='User')
    	self.profile = UserProfile.objects.create(user=self.user)
    	post = CreatePost.objects.create(user=self.profile, content="Post with comments")
    	comment = Comment.objects.create(post=post, user=self.user,text="Nice post")
    	self.assertEqual(comment.text,"Nice post")
    	self.assertEqual(comment.post,post)


       
  



   
    