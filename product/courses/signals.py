from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import Subscription, Balance
from django.conf import settings
from .models import Group


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(user=instance)


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """
    if created:
        group = Group.objects.filter(product=instance.courses.id)
        list_group = {}
        text = []
        for g in group:
            text.append(str(g))
        for word in text:
            list_group[word.split(' ')[0]] = int(word.split(' ')[-1])
        record = Group.objects.get(title=min(list_group, key=lambda k: list_group.get(k)))
        record.client.add(instance.user.id)
