from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, type, bio, address, phone_number, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        user = self.model(
            email=email,
            username=username,
            bio=bio,
            address=address,
            phone_number=phone_number,
            type=type,

        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password,
            bio='bio',
            address='address',
            phone_number='phone_number',
            type=Type.REGULAR
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Type(models.TextChoices):
    COMPANY = 'Com', 'Company'
    REGULAR = 'Reg', 'Regular'


class User(AbstractUser):
    objects = MyUserManager()

    type = models.CharField(max_length=3,
                            choices=Type.choices,
                            default=Type.REGULAR)
    bio = models.TextField(max_length=1000)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])


class Position(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    apply_link = models.URLField()
    final_apply_date = models.DateField()
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='positions')

    def get_absolute_url(self):
        return reverse('position-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title
