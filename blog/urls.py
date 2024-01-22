from django.urls import path 
from . import views

app_name='blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name="blog_home"),
    path('blog_detail/<int:pk>/', views.BlogDetailView.as_view(),name='blog_detail'),
    path('create_new_post/', views.BlogCreateView.as_view() ,name='create_new_post'),
    path('update_post/<int:pk>/', views.BlogUpdateView.as_view(), name='update_post'),
    path('delete_post/<int:pk>/', views.BlogDeleteView.as_view() ,name='delete_post')
]