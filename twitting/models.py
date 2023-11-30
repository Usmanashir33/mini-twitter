from django.db import models
from django .urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
#User = get_user_model()
from django.conf import settings
User = settings.AUTH_USER_MODEL


# Create your models here.
class Post(models.Model) :
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    text = models.TextField(help_text="Write Your Post Here!",max_length=100)
    post_file= models .FileField(upload_to="post_media",null=True,blank=True)
    post_date=models.DateTimeField(auto_now_add=True)
    likes =models.ManyToManyField(User,related_name="post_likes",blank=True)
    views=models.PositiveBigIntegerField(blank=True,default=0)
    repost=models.ManyToManyField(User,related_name='reposts',blank=True)
    
    def total_repost(self) :
        return self.repost.count()
     
    def total_views(self) :
        total_views= self.views
        return total_views
    
    def total_likes(self):
        return self.likes.count()
    
    def display_post(self):
        return self.text[:30]
    
    
    def get_absolute_url(self):
        return reverse("post-detail", args=[str(self.id)])
    
    def __str__(self):
        return self.text[:40]

    # get post comments here
    def get_comments(self):
        return Comment.objects.filter(parent=None).filter(post=self.id)
    
    def total_comments(self) :
        my_comments = Comment.objects.filter(post=self.id)
        return my_comments.count()
    
    class Meta :
        ordering=["-post_date"]
        verbose_name = "Tweet"
        
class Comment(models.Model) :
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(help_text="Comment Here!",max_length=100)
    comment_date=models.DateTimeField(auto_now_add=True)
    comment_file=models.FileField(upload_to="comments_media",null=True,blank=True)
    likes =models.ManyToManyField(User,related_name="comment_likes",blank=True)
    # make right to the reply here for any comment
    parent=models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)
    views=models.PositiveBigIntegerField(blank=True,default=0)
    repost=models.ManyToManyField(User,related_name='comment_reposts',blank=True)
    
    def total_repost(self) :
        return self.repost.count()
    
    def total_views(self) :
        total_views= self.views
        return total_views
    
    def display_comment(self) :
        return self.text[:25]
    
    def display_poster(self) :
        return self.post.user
    
    def total_likes(self) :
        return self.likes.count()
    
    class Meta :
        ordering= ["-comment_date"]
        
    def get_absolute_url(self):
        return reverse("comment-detail", kwargs={"pk": self.pk})
        
    def __str__(self):
        return self.text[:40]
    
    def get_replies(self):
        return Comment.objects.filter(parent=self)
