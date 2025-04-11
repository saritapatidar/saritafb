from django.contrib.auth.base_user import BaseUserManager


class UserManagercustom(BaseUserManager):
    def create_user(self,phone_number=None,password=None,**extra_fields):

        # extra_fields['email']=self.normalize_email(extra_fields['email'])
        user=self.model(phone_number=phone_number,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_superuser(self,phone_number=None,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)

        return self.create_user(phone_number,password,**extra_fields)
    
    # def authenticate(self, request, phone_number=None, password=None):
    #     try:
    #         user = self.get(phone_number=phone_number)
    #         if user.check_password(password):  
    #             return user
    #     except self.model.DoesNotExist:
    #         return None
    

    

        
        

