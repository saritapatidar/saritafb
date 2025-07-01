from django.apps import AppConfig

class FbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fb'

    def ready(self):
        import fb.signals  



# class MyAppConfig(AppConfig):
#     name = 'fb'

#     def ready(self):
#         from allauth.account.models import EmailAddress  # ✅ Correct
#         # now use it safely
