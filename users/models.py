# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Адрес email должен быть указан")

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, phone, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField("Email адрес", unique=True)
    phone = models.CharField(
        "Номер телефона", max_length=20, unique=True, blank=True, null=True
    )
    default_address = models.TextField(
        "Адрес доставки по умолчанию", blank=True, null=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]
    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.email or f"Пользователь {self.id}"
