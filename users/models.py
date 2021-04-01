from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from PIL import Image


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, date_of_birth, password=None, **other_fields):
        if not email:
            raise ValueError("Email is an required field!")
        if not username:
            raise ValueError("Username is a required field")
        if not first_name:
            raise ValueError("First name is an required field!")
        if not last_name:
            raise ValueError("Last name is a required field")
        if not date_of_birth:
            raise ValueError("Date of birth is an required field!")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            **other_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # creates a superuser for the project
    def create_superuser(self, email, username, first_name, last_name, date_of_birth, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name = first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# stores admin etails of all users 
class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.TextField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.TextField(max_length=30)
    last_name = models.TextField(max_length=30)
    date_of_birth = models.DateField(verbose_name="date of birth")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "date_of_birth"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

# stores user's profile picture
class Profile(models.Model):
    """
    A model that has the profile of a user
    """
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    image = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f'{self.user.email} Profile'
