import hashlib

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField('auth.User')

    class Meta:
        ordering = ['user', 'id']

    @models.permalink
    def get_absolute_url(self):
        return 'accounts:detail', (), {'username': self.user.username}

    @models.permalink
    def get_update_url(self):
        return 'accounts:update', (), {}

    def get_gravatar_url(self):
        return "https://www.gravatar.com/avatar/" + hashlib.md5(self.user.email.lower()).hexdigest()

    def __unicode__(self):
        return self.user.username


@receiver(post_save, sender=User, dispatch_uid='create_profile_on_user_create')
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
