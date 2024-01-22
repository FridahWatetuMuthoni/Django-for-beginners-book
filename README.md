# Django-for-beginners-book

## How to deal with static files during production

1. Add the following settings into your settings file

```python

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles" # new
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage" # new

```

2. compile all the static files throughout the project into a single directory

> > > python manage.py collectstatic

3. install whitenoise

> > > pip install whitenoise

4. Make the following changes
   1. add whitenoise to the INSTALLED_APPS above the built-in staticfiles app
   2. under MIDDLEWARE add a new line for WhiteNoiseMiddleware
   3. change STATICFILES_STORAGE to use WhiteNoise

```python

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #installed apps
    "whitenoise.runserver_nostatic",

    #custom apps
    'pages.apps.PagesConfig',
    'blog.apps.BlogConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", #added
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#static settings

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_ROOT = BASE_DIR / 'statcfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" # new

```

## SOME GOOD CODE SNIPPETS

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView


class ArticleCreateView(LoginRequiredMixin ,CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#UserPassesTestMixin makes sure that only the login user has the permission to
#edit his articles and only his
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body')

    def test_func(self):
        obj = self.get_object()
        return obj.author = self.request.user

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy("article_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author = self.request.user

"""
When using mixins with class-based views the order is very important. LoginRequiredMixin
comes first so that we force log in, then we add UserPassesTestMixin for an additional layer of functionality on top of it, and finally either UpdateView or DeleteView. If you do not have this order in place the code will not work properly.
"""

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'

    #adding info to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm
        return context

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin


class CommentGet(DetailView):
    model = Article
    template_name = 'article_detail.html'

    #adding info to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm
        return context

class CommentPost():
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk": article.pk})

"""
At the top import FormView, SingleObjectMixin, and reverse. FormView relies on form_class to
set the name of the form we’re using, CommentForm. First up is post(): we use get_object() from
SingleObjectMixin that lets us grab the article pk from the URL. Next is form_valid(), which is
called when form validation has succeeded. Before we save our comment to the database we have
to specify the article it belongs. Initially we save the form but set commit to False because in the
next line we associate the correct article with the form object. Then in the following line we save
the form. Finally we return it as part of form_valid(). The final module is get_success_url()
which is called after the form data is saved. We just redirect the user to the current page in this
case.
"""
class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)

"""
Deployment Checklist:
• install Gunicorn
• create a requirements.txt file
• update ALLOWED_HOSTS in django_project/settings.py
• create a Procfile file
• create a runtime.txt file
• configure static files, install whitenoise, and run collectstatic
• create and update a .gitignore file
• create a new Heroku project, push the code to it, and start a dyno web process
"""
```

## GIT / GIHUB

```git
>>> git init
>>> git add .
>>> git commit -m 'intial commit
>>> git remote add origin https://github.com/wsvincent/hello-world.git
>>> git branch -M main
>>> git push -u origin main

```

## Django Tests

Testing can be divided into two main categories: unit and integration. Unit tests check a piece of functionality in isolation, while Integration tests check multiple pieces linked together. Unit tests run faster and are easier to maintain since they focus on only a small piece of code. Integration tests are slower and harder to maintain since a failure doesn’t point you in the specific direction
of the cause. Most developers focus on writing many unit tests and a small amount of integration tests.
Generally speaking, SimpleTestCase is used when a database is not necessary while TestCase
is used when you do want to test the database. TransactionTestCase is useful if you need to
directly test database transactions while LiveServerTestCase launches a live server thread useful for testing with browser-based tools like Selenium.

## How to learn tests

> > > python manage.py test
