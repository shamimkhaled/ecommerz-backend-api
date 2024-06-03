import uuid
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# ========================UserAccountManager===============================
# for super admin user model
class UserAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email addres')
        if not username:
            raise ValueError('User must have an unique username') 
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            **extra_fields
            
        )

        user.set_password(password)
        user.save(using = self._db)

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            is_admin = True,
            is_active = True,
            is_staff = True,
            is_superadmin = True,
            is_superuser = True,

        )
        
        #user.save(using = self._db)
        return user
       
       
        
 

# ========================UserAccount===============================
# for custom user model
class UserAccount(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    # user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=50)
    

    #required
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    # change username field to replace email field and other required fiels
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

   

    def __str__(self):
        return self.email

    # if the user is admin, he has to all permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True 



# ========================UserProfile===============================
class UserProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='userprofile')
    username = models.CharField(max_length=100, blank=False, null=False)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(max_length=300, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=15, blank=True, null=True)
    
    user_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)


    date_joined = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        user_first_name = self.user.first_name
        user_last_name = self.user.last_name

        user_email = self.user.email
        split_username = user_email.index('@')
        get_username = user_email[:split_username]
        self.username = get_username
        return super().save(*args, **kwargs)

    @receiver(post_save, sender=UserAccount)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(
                user=instance,
                first_name=instance.first_name,
                last_name=instance.last_name
                
                
                )


    @receiver(post_save, sender=UserAccount)
    def save_profile(sender, instance, **kwargs):
        instance.userprofile.save()