from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from .manager import UserManagercustom
# from manager import UserManager
# import phonenumbers
# from phonenumber_field.validators import validate_international_phone_number
# from phonenumber_field.widgets import PhoneNumberWidget
 
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

                      
class CustomUser(AbstractBaseUser):
    Firstname = models.CharField(max_length=10, blank=False, null=False, default="")
    Surname = models.CharField(max_length=10, blank=False, null=False, default="")
    Date_of_birth = models.DateField(max_length=10, default="2000-08-01", blank=True, null=True)
    FEMALE = 'FEMALE'
    MALE = 'MALE'
    CUSTOM = 'CUSTOM'
    NONE = 'NONE'

    GENDER = [
        (FEMALE, "Female"),
        (MALE, "Male"),
        (CUSTOM, "Custom"),
        (NONE, "Prefer not to say"),
    ]

    gender = models.CharField(
        max_length=20,
        choices=GENDER,
        default=NONE,
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=12 ,unique=True,null=True) 
    # phone_number = models.CharField(max_length=20, blank=True, null=True, validators=[validate_international_phone_number], widget=PhoneNumberWidget())
    password = models.CharField(max_length=8,null=False,blank=True)
    is_active = models.BooleanField(default=True) 
    # is_active is a boolean field that indicates whether a user account is considered active,
    is_staff = models.BooleanField(default=False)
    # In Django is_staff is used to determine if a user can log in to the Django admin panel.
    is_superuser = models.BooleanField(default=False)
    

    last_login = None

    # USERNAME_FIELD='phone_number'
    USERNAME_FIELD='phone_number'
    REQUIRED_FIELDS=['email']
    # objects = models.Manager()
    objects = UserManagercustom()

    def __str__(self):
        return self.email 
    
    def has_module_perms(self,is_label):
        return self.is_staff
    
    def has_perm(self,perm):
        return self.is_superuser

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    

class create_post(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    content=models.TextField()
    image=models.ImageField(upload_to='post/',blank=True,default=" ")

    def __str__(self):
        return f'{self.user.username} post'

    

