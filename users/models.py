from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


class Follow(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user_id', 'following_user_id']
        ordering = ['-createdAt']

    def __str__(self):
        return self.user_id.username + ' -> ' + self.following_user_id.username


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    bio = models.CharField(max_length=128, null=True, blank=True)
    display_name = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return 'Profile ' + str(self.id) + ': ' + self.user.username


@receiver(post_save, sender=User)
def save_new_profile(sender, instance, created, **kwargs):
    if(created):
        Profile.objects.create(user=instance, display_name=instance.username, bio='')


@receiver(post_save, sender=User)
def follow_oneself(sender, instance, created, **kwargs):
    if(created):
        Follow.objects.create(user_id=instance, following_user_id=instance)
