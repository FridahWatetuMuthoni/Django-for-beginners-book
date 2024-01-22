from django.views.generic import TemplateView, ListView
from .models import Post

class HomePageView(ListView):
    model = Post
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'