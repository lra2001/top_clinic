from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('start/<int:appointment_id>/', views.start_conversation, name='start_conversation'),
    path('archive/<int:conversation_id>/', views.archive_conversation, name='archive_conversation'),
    path('unarchive/<int:conversation_id>/', views.unarchive_conversation, name='unarchive_conversation'),
]