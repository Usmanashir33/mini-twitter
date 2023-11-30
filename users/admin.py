from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile,User

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin) :
    list_display=[
        "user",
        "nationality",
        "address",
        
    ]
    list_filter=[
        "nationality",
        "date_of_birth",
    ]
    fieldsets =(
        ("Info.",{"fields":("user","date_of_birth")}),
        ("Status",{"fields":("title",)}),
        ("Details",{"fields":("nationality","address")}),
    )
    
@admin.register(User)
class UserAdmin(UserAdmin) :
    list_display=[
        "id",
        "username",
        "first_name",
        "last_name",
        "phone_number",
        "email",
        "gender",
        #"display_followers",
    ]
    list_filter=[
        "gender",
    ]

    fieldsets =(
        ("User Info.",{"fields":(("username"),"first_name","middle_name","last_name")}),
        ("contacts",{"fields":("phone_number","email",)}),
        ("details",{"fields":("gender",)}),
        ("Profile Picture",{"fields":("user_pic",)}),
        ("Following",{"fields":("Followings",)}),
        ("Rank",{"fields":("is_superuser","is_staff",'is_active')}),
        ("Permissions",{"fields":("groups","user_permissions")}),
        ("Important Dates",{"fields":("date_joined","last_login")}),
        ("Security",{"fields":("password",)}),
    )
