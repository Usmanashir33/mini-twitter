from django import forms
from .models import Post,Comment #,Reply

class PostForm(forms.ModelForm):
    #You can some fields here and itll be in a table in the db
    class Meta:
        model = Post
        fields = ("text","post_file")
        labels={"text" :"","post_file":''}
        help_texts={"text":"","post_file":''}
        widgets={
            "text":forms.Textarea(attrs={
                "class":"form-control border-0",
                "style":"width:;box-shadow:none;caret-color:green",
                "placeholder":"What's happening?",
                "autofocus":"autofocus",
                
            }),
            "post_file":forms.FileInput(attrs={
                "class":"form-control border-0",
                "style":"",
                "placeholder":"Select File Here "
            })
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text","comment_file")
        labels={"text" :"","comment_file":""}
        help_texts={"text" :"","comment_file":""}
        widgets={
            "text":forms.Textarea(attrs={
                "class":"form-control border-0",
                "style":"width:;box-shadow:none;caret-color:green",
                "placeholder":"What's happening?",
                "autofocus":"autofocus",
                
            }),
            "comment_file":forms.FileInput(attrs={
                "class":"form-control border-0",
                "style":"",
                "placeholder":"Select File Here "
            })
        }
class ReplyForm(forms.ModelForm) :
    class Meta :
       # model = Reply
        fields =["reply"]
        labels={"reply" :""}
        help_texts={"reply" :""}
        widgets={"reply":forms.Textarea(attrs={
            "class":"form-control border-0",
            "style":"width:;box-shadow:none;caret-color:green",
            "placeholder":"Reply here",
            "autofocus":"autofocus",
            
            })}
        
    def clean_reply(self):
        data = self.cleaned_data["reply"]
        return data
    
    

