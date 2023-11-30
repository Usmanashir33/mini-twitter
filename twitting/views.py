
from typing import Any
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,BaseUpdateView
from django.contrib import messages
from .forms import PostForm
from .models import Post,Comment #,Reply
from django.urls import reverse, reverse_lazy
from django.conf import settings
User = settings.AUTH_USER_MODEL


# Create your views here.

def index(request) :
    return render(request,"twitting/index.html")

class PostListView(ListView) :
    model=Post
    def get_queryset(self):
        posts=Post.objects.all()
        for post in posts :
            post.views += 1
            post.save()
        return posts
    
    
class PostDetailView(DetailView) :
    model = Post
    def get_context_data(self, **kwargs):
        id=self.kwargs.get("pk")
        post = get_object_or_404(Post,pk=id)
        comments = post.comment_set.all()
        context = super().get_context_data(**kwargs)
        context["comments"] = comments
        
        """ make comment view here """
        for comment in post.comment_set.all() :
            comment.views += 1
            comment.save()
        return context
 
#editing post
from .forms import PostForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse

def create_post(request) :
    if request.method != "POST" :
        form =PostForm()
    else :
       form = PostForm(request.POST or None,request.FILES or None)
       if form .is_valid() :
           new_post = form.save(commit=False)
           new_post.user= request.user
           new_post.save()
           messages.success(request,"You Have Successfully Posted")
           return HttpResponseRedirect(reverse("post-list"))
       
    context ={
        "form":form
    }
    return render(request,"twitting/post_form.html",context)
from os.path import join
from django import forms
def update_post(request,pk) :
    #model = Post
    #form_class =PostForm
    #template_name_suffix="_update"
    
    post=get_object_or_404(Post,id=pk)
    post_file=post.post_file
    if request.method =="POST" :
        post_form=PostForm(request.POST or None,request.FILES or None,instance=post)
        delete_request =request.POST.get("clear_pic")
        next=request.POST.get("next")
        if post_form.is_valid():
            if post_file :
                if len(request.FILES) != 0 :
                    os.remove(post_file.path)
                else :
                    try :
                        if delete_request == "delete" :
                            os.remove(post_file.path)
                            post_file.delete(save=True)
                    except Exception :
                        pass
            post_form.save()
            messages.success(request,"Post Updated Successfully")
            #return redirect(reverse("post-list") +'#'+str(pk))
            return redirect(next)# +'#'+str(pk))
    else :
        post_form=PostForm(instance=post)
    context={
        "form":post_form,
        "post":post,
    }
    return render(request,"twitting/post_update.html",context)

    #def get_success_url(self):
      #   post_id=self.kwargs.get("pk")
      #   return join(reverse("post-list") +"#"+str(post_id))
     
class DeletePost(DeleteView) :
     model = Post
     fields= ["post"]
     success_url = reverse_lazy("post-list")
     
def post_likes(request,pk) :
    next=request.GET.get("next","/")
    user= request.user
    post=get_object_or_404(Post,id=pk)
    post_likes = post.likes
    if request.method == "GET" :
        if post_likes.filter(id=user.id) :
            post_likes.remove(user)
        else :
            post_likes.add(user)
        return redirect(next)
    
def repost(request,pk) :
    next=request.GET.get("next","/")
    post=Post.objects.get(id=pk)
    reposts=post.repost
    if request.method != "POST" :
        if  request.user in reposts.filter(id=request.user.id) :
            reposts.remove(request.user)
        else :
            reposts.add(request.user)
    return redirect(next)

""" Comment section"""
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
def create_comment(request,post_id) :
    post_of_comment=get_object_or_404(Post,id=post_id)
    if request.method != "POST" :
        form = CommentForm()
    else :
        next=request.POST.get("next","/")
        form = CommentForm(request.POST or None,request.FILES or None)
        if form.is_valid() :
            new_comment = form.save(commit=False)
            new_comment.user=request.user
            new_comment.post=post_of_comment
            new_comment.save()
            messages.success(request,f"Comment Sent to {new_comment.user}")
            #return redirect(reverse("post-list") +'#'+str(post_of_comment.id))
            return redirect(next +'#'+str(post_of_comment.id))
    context ={
        "form" :form,
        "post" :post_of_comment,
    }
    return render(request,"twitting/create_comment.html",context)
import os
def update_comment(request,pk) :
    comment=get_object_or_404(Comment,pk=pk)
    comment_file=comment.comment_file
    post_id = comment.post.id
    if request.method != "POST" :
        form =CommentForm(instance=comment)
    else :
        form=CommentForm(request.POST,request.FILES,instance=comment)
        clear_pic = request.POST.get("clear_pic",None)
        next=request.POST.get("next")
        if form.is_valid() :
            if len(request.FILES) != 0 :
                try :
                    if comment_file :
                        os .remove(comment_file.path)
                except Exception :
                    pass
            else :
                if  clear_pic != "delete":
                    pass
                else :
                    os.remove(comment_file.path)
                    comment_file.delete()
                
            form.save()
            messages.success(request,"Comment Updated Successfully!")
            return redirect(next) 
    context={
        "form":form,
        "comment":comment,
    }
    return render(request,"twitting/comment_update.html",context)
        
def delete_comment(request,pk) :
    comment = get_object_or_404(Comment,pk=pk)
    post_id=comment.post.id
    if request.method == 'POST' :
        comment.delete()
        messages.success(request,"Deleted Successfully")
        return redirect('post-detail',pk=post_id)
    context ={
        "comment":comment,
    }
    return render(request,"twitting/comment_confirm_delete.html",context)

class CommentDetailView(DetailView):
    model= Comment
    
def comment_likes(request,pk) :
    next_page=request.GET.get("next","/")
    comment=get_object_or_404(Comment,id=pk)
    likes=comment.likes
    if request.method != "POST" :
        if likes.filter(id=request.user.id) :
            likes.remove(request.user)
        else:
            likes.add(request.user)
    return redirect(next_page)       

def comment_repost(request,pk) :
    next=request.GET.get("next","/")
    comment=Comment.objects.get(id=pk)
    Reposts=comment.repost
    if request.method != "POST" :
        if  request.user in Reposts.filter(id=request.user.id) :
            Reposts.remove(request.user)
        else :
            Reposts.add(request.user)
    return redirect(next)    
    

""" reply section"""
from .forms import ReplyForm
def add_reply(request,pk) :# pk for comment
    comment= get_object_or_404(Comment,pk=pk)
    post_id= comment.post.id
    comment_post=get_object_or_404(Post,pk=post_id)
    comment_post_url=comment_post.get_absolute_url()
    comment_url=comment.get_absolute_url()
    
    if request.method != "POST" :
        form = CommentForm()
    else :
        next= request.POST.get("next","post-list")
        form=CommentForm(request.POST or None,request.FILES or None)
        if form.is_valid() :
            reply=form.save(commit=False)
            reply.user = request.user
            reply.post = comment_post
            reply.parent=comment
            reply.save()
            messages.success(request, f"Reply sent to {reply.user}")
            return redirect(next +"#"+str(comment.id))
    context ={
        "comment" :comment,
        "form" :form
    }
    return render(request,"twitting/create_comment.html",context)
