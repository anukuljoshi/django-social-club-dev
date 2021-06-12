from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)


class Downvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    # image = models.ImageField()
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    upvoted_by = models.ManyToManyField(User, through=Upvote, related_name='upvoter')
    downvoted_by = models.ManyToManyField(User, through=Downvote, related_name='downvoter')


    class Meta:
        ordering = ['-createdAt']

    def __str__(self):
        return 'Post ' + str(self.id) + ': ' +  self.content[:10]


    @property
    def votes(self):
        return self.upvoted_by.count() - self.downvoted_by.count()                                                                                                                                          
