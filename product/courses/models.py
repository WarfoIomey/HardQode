from django.db import models
from django.conf import settings


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name='Цена продукта'
    )
    # TODO

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.author} - {self.title} - {self.price} - {self.start_date} '


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )
    product = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    # TODO

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'{self.title} - {self.product.title} - {self.product.author}'


class Group(models.Model):
    """Модель группы."""
    # TODO
    title = models.CharField(
        max_length=250,
        verbose_name='Название группы'
    )
    product = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    client = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='client'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.title} - {self.product.title} - {self.client.count()}'