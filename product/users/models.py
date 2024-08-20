from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import Course


class CustomUser(AbstractUser):

    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):

    """Модель баланса пользователя."""

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
    )
    score = models.PositiveIntegerField(
        default=1000,
    )
    # TODO

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.score}'


class Subscription(models.Model):

    """Модель подписки пользователя на курс."""

    # TODO
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    courses = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписку'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.courses.title}'
