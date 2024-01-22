from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Blog_Post

# Create your views here.
class BlogListView(ListView):
    model = Blog_Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'

class BlogDetailView(DetailView):
    model = Blog_Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

class BlogCreateView(CreateView):
    model = Blog_Post
    template_name = 'blog/create.html'
    fields = ['title', 'author', 'body']

class BlogUpdateView(UpdateView):
    model = Blog_Post
    template_name = 'blog/update.html'
    fields = ['title','body']


class BlogDeleteView(DeleteView):
    model = Blog_Post
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('blog:blog_home')
