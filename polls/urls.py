from django.urls import path , include , re_path
from . import views
from django.contrib import admin 
from django.urls import path, include , re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "polls"

urlpatterns = [
    path('list/', views.polls_list, name='list'),
    path('list/user/', views.list_by_user, name='list_by_user'),
    path('add/', views.polls_add, name='add'),
    path('edit/<int:poll_id>/', views.polls_edit, name='edit'),
    path('delete/<int:poll_id>/', views.polls_delete, name='delete_poll'),
    path('end/<int:poll_id>/', views.endpoll, name='end_poll'),
    path('edit/<int:poll_id>/choice/add/', views.add_choice, name='add_choice'),
    path('edit/choice/<int:choice_id>/', views.choice_edit, name='choice_edit'),
    path('delete/choice/<int:choice_id>/',
         views.choice_delete, name='choice_delete'),
    path('<int:poll_id>/vote/', views.poll_vote, name='vote'),
    path('<int:poll_id>/comment/', views.comments, name='comments'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    

 
   

  
   
    
]

urlpatterns += staticfiles_urlpatterns()