from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    USER_ROLE_USER = "user"
    USER_ROLE_MODERATOR = "moderator"
    USER_ROLE_ADMIN = "admin"

    USER_ROLE_CHOICES = (
        (USER_ROLE_USER, "Пользователь"),
        (USER_ROLE_MODERATOR, "Модератор"),
        (USER_ROLE_ADMIN, "Админ"),
    )

    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(
        db_index=True,
        unique=True,
        max_length=255,
        verbose_name="Электронная почта",
    )
    role = models.CharField(
        max_length=16,
        choices=USER_ROLE_CHOICES,
        default=USER_ROLE_USER,
        verbose_name="Роль",
    )
    bio = models.TextField(blank=True, verbose_name="Описание")
    confirmation_code = models.CharField(
        max_length=50, blank=True, verbose_name="Код для авторизации"
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        """Строковое представление модели (отображается в консоли)"""
        return self.email

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_username_email"
            )
        ]

    @property
    def is_user(self):
        return self.role == self.USER_ROLE_USER

    @property
    def is_moderator(self):
        return self.role == self.USER_ROLE_MODERATOR

    @property
    def is_admin(self):
        return self.role == self.USER_ROLE_ADMIN
