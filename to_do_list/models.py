from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class CustomManager(BaseUserManager):
    def create_user(self,email,password,**extra_kwargs):
        email = self.normalize_email(email)
        user = self.model(email = email,**extra_kwargs)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,email,password,**extra_kwargs):
        extra_kwargs.setdefault('is_staff',True)
        extra_kwargs.setdefault('is_superuser',True)
        return self.create_user(email,password,**extra_kwargs)

    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200)  
    email = models.EmailField(max_length=200, unique=True)
    mobile = models.BigIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    objects = CustomManager()
    USERNAME_FIELD = 'email' 
    def __str__(self) -> str:
        
        return f"{self.id}_{self.email}_{self.name}"
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="profile")
    dob = models.DateField(null=True,blank=True)
    
    
class ListNDesc(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="ListNDesc")
    title = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)