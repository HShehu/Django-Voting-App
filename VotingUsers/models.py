from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyVotingUserManager(BaseUserManager):
    def create_user(self,student_number,full_name,login_code,password=None):

        if not student_number:
            raise ValueError("Must have a Student Number to Vote")
        if not full_name:
            raise ValueError("Must input Full Name")
        if not login_code:
            raise ValueError("Must have a Login Code to Vote")

        user = self.model(
            student_number = student_number,
            full_name = full_name,
            login_code = login_code,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,student_number,full_name,login_code,password=None):
        user = self.create_user(
            student_number = student_number,
            full_name = full_name,
            password = password,
            login_code = login_code,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class VotingUser(AbstractBaseUser):
    student_number = models.CharField(max_length=8,unique= True, verbose_name="Student Number")
    full_name = models.CharField(verbose_name="Full Name",max_length=50)
    login_code = models.PositiveSmallIntegerField(verbose_name="Login Code")
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'student_number'
    REQUIRED_FIELDS = ['full_name','login_code',]

    objects = MyVotingUserManager() 
    

    def __str__(self):
        return self.student_number + ": " + self.full_name

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True
