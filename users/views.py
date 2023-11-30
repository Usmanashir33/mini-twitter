from django.shortcuts import render,get_object_or_404
from .forms import ProfileForm,RegisterForm,UserUpdateForm,PasswordsChangingForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DetailView
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.shortcuts import redirect
from.models import Profile,User
from twitting.models import Post
from django.contrib.auth import login,logout
from django.conf import settings
#User = settings.AUTH_USER_MODEL

#to delete files
import os
# Create your views here.

def register(request) :
    if request.method != "POST" :
        form = RegisterForm()
    else :
        form=RegisterForm(request.POST or None,request.FILES or None)
        if form.is_valid() :
            form.save()
            """ logging in"""
            username=form.cleaned_data["username"]            
            password=form.cleaned_data["password1"]            
            user = authenticate(username=username,password=password)
            messages.success(request,"You have successfully logged in ")
            login(request,user)
            return redirect('fill-profile')
        
             
    context ={
        "form":form,
    }   
    return render(request,"registration/register.html",context)

from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.urls import reverse_lazy

def fill_profile(request):
    if request.method != "POST":
        form = ProfileForm()
        profile=form.save(commit=False)
        profile.user=request.user
        profile.save()
    else:
        form=ProfileForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect("index")
    context={"form":form}
    return render(request,"users/fill_profile.html",context)

class UserDetailView(DetailView):
    model=User
    template_name="users/view_user_profile.html"
    context_object_name="profile"
    def get_context_data(self, **kwargs):
        id=self.kwargs.get("pk")
        posts=Post.objects.filter(user=id)
        reposts=Post.objects.filter(repost=id)
        all_posts= list(posts) + list(reposts)
        no_all_posts=len(list(posts)) + len(list(reposts))
        #All_posts=set(all_posts) tHIS WILL REMOVE ALL THE DUPLICATES IN THE LIST OF THE POSTS AVAILABLE
        context = super().get_context_data(**kwargs)
        context["profile_posts_and_reposts"] =all_posts
        context["no_all_posts"] =no_all_posts
        return context
    
    
    
def user_profile_update(request,pk):
    user_profile=get_object_or_404(User,id=pk)
    user_profile_pic=user_profile.user_pic
    if request.method != "POST":
        u_form =UserUpdateForm(instance=user_profile)
        #check if user already has prifile
        try :
            if user_profile.profile:
                p_form=ProfileForm(instance=user_profile.profile)
        except Exception :
            p_form=ProfileForm()
    else :
        u_form =UserUpdateForm(request.POST or None,request.FILES or None ,instance=user_profile)
        
        #check if user already has prifile
        try :
            if user_profile.profile:
                p_form=ProfileForm(request.POST,request.FILES or None,instance=user_profile.profile)        
        except Exception :
            p_form=ProfileForm(request.POST,request.FILES or None)
        
        delete_pic=request.POST.get("clear_pic")
        if p_form.is_valid() and u_form.is_valid():
            #check and remove image from our files if changed or cleared
            if len(request.FILES) != 0 :
                if user_profile_pic:
                    os.remove(user_profile_pic.path)
            else :
                if delete_pic == "delete" :
                   os.remove(user_profile_pic.path)
                   user_profile_pic.delete(save=True)
            u_form.save()
            profile_form=p_form.save(commit=False)
            profile_form.user=user_profile
            profile_form.save()
            messages.success(request,"profile Update Successfully")
            return redirect("user-detail",pk=pk)
    context={
        "u_form":u_form,
        "p_form":p_form,
        "user_profile_pic":user_profile_pic
    }
    return render(request,"users/profile_update_styled.html",context)

# def view_user_profile(request,pk) :
#     user_profile=get_object_or_404(Profile,id=pk)
#     is_following=user_profile.user.Followers.filter(id=request.user.id)
#     context={
#      "profile":user_profile,  
#      "is_following":is_following,
#     }
#     return render(request,"users/view_user_profile.html",context)


def following_friend(request,pk) :
    current_user=request.user
    friend=get_object_or_404(User,id=pk)
    friend_followers=friend.followers
    Next=request.GET.get("next","/")
    if request.method != "POST" :
        if current_user in friend_followers.all():
            friend_followers.remove(current_user)
        else :
            friend_followers.add(current_user)
        return redirect(Next)
    
def followers(request,pk) :
    user = get_object_or_404(User,id=pk)
    followers = user.followers.all()
    context ={
		"followers" :followers
	}
    return render(request,"users/followers.html",context)

def followings(request,pk) :
    user = get_object_or_404(User,id=pk)
    followings = user.Followings.all()
    context ={
		"followings" :followings
	}
    return render(request,"users/followings.html",context)

def search_any_friend(request) :
    if request.method == "POST" :
        search=request.POST['search']
        words=search.split()
        all_friends=User.objects.all()
        for word in words :
            friends_found=[]
            friends= all_friends.filter(username__contains= word
                    ) or all_friends.filter(first_name__contains= word
                    )or  all_friends.filter(last_name__contains= word) 
            for friend in friends :
                if friend  not in friends_found :
                    friends_found.append(friend)
    else :
         friends_found=[]
         search='a'
    context={
      "friends":friends_found[::-1],
      "word":search  
    }
    return render(request,"users/search_any_friend.html",context)

""" setting section"""
def settings(request):
    context={
        
    }
    return render(request,"users/settings.html",context)

""" logging in and out"""
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("log-in")
    return render(request,'registration/logout.html')

def user_login(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None :
            login(request,user)
            messages.success(request,"You have logged in")
            return redirect("index")
    else :
        pass
    return render(request,'registration/login.html')

class PasswordsChangingView(PasswordChangeView):
    form_class = PasswordsChangingForm
    template_name = "registration/change_password.html"
    success_url=reverse_lazy("settings")