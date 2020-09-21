from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    slug = models.CharField(max_length=130,default="")

    def __str__(self):
        return self.name

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    serial = models.IntegerField(default=1)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    likes = models.ManyToManyField(User ,related_name='likes', blank=True)
    content = models.TextField()
    authur = models.CharField(max_length=13)
    slug = models.CharField(max_length=130)
    views = models.IntegerField(default=0)
    timeStamp = models.DateTimeField(blank=True)


    def __str__(self):
        return  self.title + '  by ' + self.authur
     
    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment',null=True, related_name="replies",on_delete=models.CASCADE )
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)#Oner to one set profile with user
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return "Profile of user {}".format(self.user.username)