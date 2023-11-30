""" form file """
from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from . models import  User

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#PHONE NUMBER FIELD
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
# country selection
from django_countries.fields import CountryField
#from django_countries.widgets import CountrySelectWidget


class RegisterForm(UserCreationForm):
    Gend=(("M","male"),("F","female"),("O","others"),)
    username=forms.CharField(label="",widget=forms.TextInput(attrs={"class":"form-control mb-4","placeholder":"Username"}))
    first_name=forms.CharField(label="",widget=forms.TextInput(attrs={"class":"form-control mb-4","placeholder":"First Name"}))
    #middle_name=forms.CharField(label="",widget=forms.TextInput(attrs={"class":"form-control mb-4","placeholder":" Middle Name (optional)"}))
    last_name=forms.CharField(label="",widget=forms.TextInput(attrs={"class":"form-control mb-4","placeholder":"Last Name"}))
    gender=forms.ChoiceField(choices=Gend,label="",widget=forms.Select(attrs={"class":"form-control mb-4","placeholder":"Gender"}))
    email=forms.CharField(label="",widget=forms.EmailInput(attrs={"class":"form-control mb-4","placeholder":"Email address(e.g minitwitter@gmail.com) "}))
    #user_pic=forms.ImageField(label="",widget=forms.FileInput(attrs={"type":"file","class":"form-control form_control-md mb-4","placeholder":"Profile Pic"}))
    password1=forms.CharField(label="",widget=forms.TextInput(attrs={"type":"password","class":"form-control mb-4", "placeholder":"Password"}))
    password2=forms.CharField(label="",help_text="Must be the same with your password Must be 8+,alpha,numeric,and characters only",
                              widget=forms.TextInput(attrs={"type":"password","class":"form-control mb-4","placeholder":"Confirm The above Password"}))
    Countary_choices=(("NIG","+234"),("NGR","+224"))
    phone_number=PhoneNumberField(max_length=20,label="",
                                widget=PhoneNumberPrefixWidget(
                                attrs={"class":"form-control mb-4","placeholder":" Phone Number(e.g 8166997172) "}))
    
    class Meta :
        model = User
        fields=[
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "phone_number",
            "email",
            "password1",
            "password2",
            "user_pic",
        ]
        
    def clean_email(self) :
        data=self.cleaned_data["email"]
        emails=[user.email for user in User.objects.all()]
        if data in emails :
            raise ValidationError(_("This email is already linked to another account "))
        return data
    def clean_phone_number(self) :
        data=self.cleaned_data["phone_number"]
        phone_numbers=[user.phone_number for user in User.objects.all()]
        if data in phone_numbers :
            raise ValidationError(_("This Phone number is already linked to another account "))
        return data
    
import datetime
class ProfileForm(forms.ModelForm) :
    class Meta :
        model = Profile
        fields=[
            "title",
            "date_of_birth",
            "nationality",
            "address",
        ]
        widgets ={
            "date_of_birth":forms.DateInput(attrs={"type":"date", "class":"form-control mb-4","placeholder":"Date Of Birth must be above 16"}),
            "nationality":forms.Select(attrs={"class":"form-control mb-4", "placeholder":"Country of Residence"}),
            "address":forms.TextInput(attrs={"class":"form-control mb-4","placeholder":"Address Must Be With House no (124 sk block line)"}),
            "title":forms.TextInput(attrs={"class":"form-control mb-4","placeholder":"Prepare Youre Title"}),
        }
        labels={
            "title":"",
            "date_of_birth":"",
            "nationality":"",
            "address":"",
        }
        help_texts={
            "title":"",
            "date_of_birth":"",
            "nationality":"",
            "address":"",
            
        }
        
    def clean_date_of_birth(self):
        data=self.cleaned_data["date_of_birth"]
        """ checking the range"""
        
        if data :
            if data > datetime.date.today() - datetime.timedelta(days=5844) :
                raise ValidationError(_("Must be Above 16 years"))
            return data
    
    def clean_address(self):
        data=self.cleaned_data['address']
        with_number = []
        if data :
            for i in range(10) :
                if str(i) in data[:8] :
                    with_number.append(i)
            if with_number :
                pass
            else :
                raise ValidationError(_("address must contain house number at the beggining"))
            return data
      
class UserUpdateForm(forms.ModelForm):
    class Meta :
        model = User
        fields= ["username","first_name","middle_name",'last_name',"gender","phone_number","email","user_pic"]
        Countary_choices=(("NIG","+234"),("NGR","+224"))
        widgets ={
            "username":forms.TextInput(attrs={"class":"form-control mb-4 form-floating ", "placeholder":"150 characters or fewer. Letters, digits and @/./+/-/_ only"}),
            "first_name":forms.TextInput(attrs={"class":"form-control mb-4","placeholder":"Your First Name",}),
            "middle_name":forms.TextInput(attrs={"class":"form-control mb-4","placeholder":"Your First Name",}),
            "last_name":forms.TextInput(attrs={"class":"form-control mb-4","placeholder":"Your Last Name"}),
            "gender":forms.Select(attrs={"class":"form-control mb-4","placeholder":"Gender"}),
            "email":forms.EmailInput(attrs={"class":"form-control mb-4","placeholder":"Avalid Email Address"}),
            "user_pic":forms.FileInput(attrs={"type":"file","class":"form-control form_control-md mb-4","placeholder":"Profile Pic"}),
            "phone_number":PhoneNumberPrefixWidget(
                                    attrs={"class":"form-control mb-4",
                                            "placeholder":" Phone Number(e.g 8166997172) "})
        }
        labels={
            "username":"",
            "first_name":"",
            "middle_name":"",
            "last_name":"",
            "gender":"",
            "phone_number":"",
            "email":"",
            "user_pic":"",
        }
        help_texts={
            "username":"",
            "first_name":"",
            "middle_name":"",
            "last_name":"",
            "gender":"",
            "phone_number":"",
            "email":"",
            "user_pic":"",
        }
        
class PasswordsChangingForm(PasswordChangeForm) :
    old_password = forms.CharField( label="",widget=forms.PasswordInput(attrs={"class":"form-control mb-3 form-floating ", "placeholder": "Enter Your Old Password"}))
    new_password1 = forms.CharField(label="",max_length=100, widget=forms.PasswordInput(attrs={"class":"form-control mb-3","placeholder":"Create New Password","help_text":"tttt"}))
    new_password2 =forms.CharField(label="",max_length=100, widget=forms.PasswordInput(attrs={"class":"form-control mb-3","placeholder":"Confirm Your New Password"}))
    class Meta :
        model=User
        fields=("old_password","new_password1","new_password2")
           