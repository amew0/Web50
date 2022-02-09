from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime    
from django.forms import ModelForm, Textarea

class User(AbstractUser):
    follower = models.ManyToManyField('self', symmetrical = False, related_name = "following")
    
    def serialize(self):
        return {
        "id": self.id,
        "username": self.username,
        "email":self.email,
        "follower":[aFollower.id for aFollower in self.follower.all()],
        "following":[following.id for following in self.following.all()]
        }
class Post(models.Model):
    content = models.TextField()
    userP = models.ForeignKey(to='network.User', on_delete=models.CASCADE, related_name="userspost")
    likes = models.IntegerField(default=0)
    dateNtime = models.DateTimeField(default=datetime.now) #2018-11-20T15:58:44

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "userP" : self.userP.username,
            "likes": self.likes,
            "dateNtime": self.dateNtime,
        }
class PostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'cols': 80, 'rows': 20, 'placeholder': 'What"s happenning?'}),
        }