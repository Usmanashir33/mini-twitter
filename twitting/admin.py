from django.contrib import admin
from .models import Post,Comment #SReply

# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    fieldsets = (
        ("Details", {
            "fields": (
              ("user","post")  
            ),
        }),
        ("Message",{"fields":("text","comment_file")})
    )
    extra=0
    
#class ReplyInline(admin.StackedInline):
   # model = Reply
    #extra=0
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin) :
    list_display=["display_post","user","post_date"]
    list_filter=["post_date"]
    inlines=[CommentInline]
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin) :
    list_display=["display_comment","user","comment_date","post","display_poster"]
    list_filter=["comment_date"]
    fieldsets = (
        ("Details", {
            "fields": (
              ("user","post","parent")  
            ),
        }),
        ("Message",{"fields":("text","comment_file")})
    )
    
"""
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin) :
    pass
    list_display=['display_reply',"user","reply_date","post","display_comment","display_commenter"]
    list_filter=["reply_date"]
    fieldsets = (
        ("Details", {
            "fields": (
              ("user","comments","post")  
            ),
        }),
        ("Message",{"fields":("reply",)})
    )
"""