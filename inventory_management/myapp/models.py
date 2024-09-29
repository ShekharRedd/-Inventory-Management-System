from django.db import models

# models.py (Django ORM or SQLAlchemy if you are not using Django)
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import bcrypt

from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        
        user.set_password(password)  # Password hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)  # Default value for existing rows
    updated_at = models.DateTimeField(auto_now=True)
    
    # User Manager
    objects = UserManager()

    # Define how Django will identify the user (email in this case)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """Hash the password before saving."""
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        """Check if the provided password matches the stored password."""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))



class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
