from django.urls import path

from . import views

urlpatterns = [    

    path('<str:username>/<int:post_id>/edit/', views.post_edit,
         name='post_edit'),
    path('<str:username>/<int:post_id>/delete/', views.post_delete,
         name='post_delete'), 
    path('new/', views.new_post, name='new_post'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),

    path("", views.index, name="index"),    
    path('<str:username>/', views.profile, name='profile'),
     ]
