from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
User = settings.AUTH_USER_MODEL

# Create your models here.
class User(AbstractUser):
    Gend=(("M","male"),("F","female"),("O","others"),)
    gender=models.CharField(max_length=2,choices=Gend,default="M",null=True,blank=True)
    middle_name=models.CharField(max_length=40,blank=True,null=True)
    phone_number=PhoneNumberField(blank=True,max_length=20,region="CA")
    user_pic=models.ImageField(upload_to="images",blank=True,null=True)
    # follow machine
    Followings=models.ManyToManyField(User,related_name="followers",verbose_name=(""),blank=True)
    
    
    class Meta :
        db_table='auth_user'
        ordering=['first_name',]
    
    def total_followers(self):
        return self.followers.count()
    
    def total_followings(self):
        return self.Followings.count()
    
    def display_followers(self) :
        followers=[x for x in self.Followers.all()]
        return followers
        
    def get_absolute_url(self):
        return reverse("user-detail", args=[str(self.id)])
    
    def __str__(self):
        if self.middle_name :
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else :
            return f"{self.first_name} {self.last_name}"
        
class Profile(models.Model):
    Countries=(
        ("Nig","Nigeria"),
        ("Niger","Niger"),
        ("Saudia","Saudi Arabia"),
        ("Uk","United Kingdom"),
        ("USA","United State"),
        ("other","Others"),
    )
    user=models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
    date_of_birth=models.DateField("D.O.B",help_text="write your dob must be above 16",null=True,blank=True)
    nationality=CountryField(max_length=30,default="NG")
    address =models.CharField(max_length=100,help_text="write your full adress,house number must be included",null=True,blank=True)
    title=models.CharField(max_length=100,blank=True)
    class Meta :
        ordering=['nationality']
        
    def get_absolute_url(self):
        return reverse("profile-detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f"{self.nationality} @ {self.address}"
    
