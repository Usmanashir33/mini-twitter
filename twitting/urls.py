""" The twitting app urls"""
from django .urls import path,include
from . import views


urlpatterns = [
    path("",views.index,name="index"),
    #""" Post section"""
    path("addpost/",views.create_post,name="add-post"),
    path("postlist/",views.PostListView.as_view(),name="post-list"),
    path("postdetail/<int:pk>",views.PostDetailView.as_view(),name="post-detail"),
    path("updatepost/<int:pk>",views.update_post,name="update-post"),
    path("deletepost/<int:pk>",views.DeletePost.as_view(),name="delete-post"),
    path("postLikes/<int:pk>",views.post_likes,name="post-likes"),
    path("reposting/<int:pk>",views.repost,name="repost"),
    
    #""" Comment Section"""
    path("addcomment/<int:post_id>",views.create_comment,name="add-comment"),
    path("updatecomment/<int:pk>",views.update_comment,name="update-comment"),
    path("deletecomment/<int:pk>",views.delete_comment,name="delete-comment"),
    path("commentdetail/<int:pk>",views.CommentDetailView.as_view(),name="comment-detail"),
    path("commentLikes/<int:pk>",views.comment_likes,name="comment-likes"),
    path("creposting/<int:pk>",views.comment_repost,name='comment_reposts'),
    
    # """ Reply Section"""
    path("addreply/<int:pk>",views.add_reply,name="add-reply"),
    #path("update/<int:pk>",views.UpdateView.as_view(),name="update-reply"),
    #path("delete/<int:pk>",views.DeleteView.as_view(),name="delete-reply"),
    #path("replydetail/<int:pk>",views.reply_detail,name="reply-detail"),
    
]
