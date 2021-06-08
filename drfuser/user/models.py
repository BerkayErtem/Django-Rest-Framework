from django.db import models
from django.contrib.auth.models import(AbstractBaseUser,BaseUserManager,PermissionsMixin)
from django.db.models.fields import EmailField
from phone_field import PhoneField

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,  username, password=None):
        if username is None:
            raise TypeError('username required')

        user=self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, username, password):
        if password is None:
            raise TypeError('password required')
        user=self.create_user(username, password)
        user.is_admin=True
        user.is_superuser=True
        user.is_staff=True

        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    username=models.CharField(max_length=50, unique=True)
    created_at=models.DateField(auto_now=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')

    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    company_name=models.ForeignKey('Company',on_delete=models.CASCADE, blank=True, null=True)

    USERNAME_FIELD='username'
    
    objects=UserManager()
    def __str__(self):
        return self.username
    
    
class Company(models.Model):
    companyTitle= models.CharField(max_length=20,primary_key=True, serialize=False, verbose_name='Company Title')
    companyName=models.CharField(max_length=250, blank=False)
    taxOffice=models.CharField(max_length=250, blank=False)
    taxNumber=models.CharField(max_length=100,blank=False)
    tel=models.CharField(max_length=100)
    email=models.EmailField(max_length=150)
    address=models.CharField(max_length=500, blank=False)
    class Meta:
        db_table="Company"
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)   
    def __str__(self):
        return self.companyTitle
        
class Subsidiary(models.Model):
    subsidiaryTitle= models.CharField(max_length=20,primary_key=True, serialize=False, verbose_name='Subsidiary Title')
    companyName=models.ForeignKey('Company',on_delete=models.CASCADE, blank=True, null=True)
    subsidiaryName=models.CharField(max_length=250, blank=True)
    sub_taxOffice=models.CharField(max_length=250)
    sub_taxNumber=models.CharField(max_length=100)
    sub_tel=models.CharField(max_length=100)
    sub_email=models.EmailField(max_length=150)
    sub_address=models.CharField(max_length=500, blank=False)
    class Meta:
        db_table='Subsidiary'
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)   
    def __str__(self):
        return self.subsidiaryTitle

class Image(models.Model):
    image_name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='images/')
    class Meta:
        db_table="images"

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)   
    def __str__(self):
        return self.image_name

class Form(models.Model):
    id=models.AutoField(auto_created=True, primary_key=True ,unique=True, max_length=50)
    approval=models.BooleanField(default=False)
    destination=models.CharField(max_length=50, blank=False)
    date=models.DateField(blank=False)
    class Meta:
        db_table='forms'
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs) 
    def __str__(self):
        return self.destination