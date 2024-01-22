from urllib import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Blog_Post
from django.urls import reverse

class BlogTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username = 'testuser',email="testuser@gmail.com", password='secret'
        )
        
        cls.post =Blog_Post.objects.create(
            title='A good title',
            body='Nice body content',
            author = cls.user
        )
    
    def test_blog_model(self):
        self.assertEqual(self.post.title, 'A good title')
        self.assertEqual(self.post.body, 'Nice body content')
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertEqual(str(self.post), 'A good title')
        self.assertEqual(self.post.get_absolute_url(), '/blog/blog_detail/1/')
    
    def test_url_exits_at_correct_location_listview(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
    
    def test_url_exits_at_correct_location_detailview(self):
        response = self.client.get('/blog/blog_detail/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_blog_listview(self):
        #response = self.client.get(reverse('blog:blog_home'))
        response = self.client.get(reverse('blog:blog_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response, 'Nice body content')
        
    def test_blog_detailview(self):
        response = self.client.get(reverse('blog:blog_detail', kwargs={'pk': self.post.pk}))
        no_response = self.client.get('/blog/blog_detail/10000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'blog/blog_detail.html')
        self.assertContains(response, 'A good title')
    
    def test_post_createview(self):
        response = self.client.post(
            reverse('blog:create_new_post'),
            {
                'title':'New title',
                "body":'New text',
                'author':self.user.id
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog_Post.objects.last().title , 'New title')
        self.assertEqual(Blog_Post.objects.last().body , 'New text')
    
    def test_post_updateview(self):
        response = self.client.post(
            reverse('blog:update_post', kwargs={'pk': 1}),
            {
                'title':'updated title',
                "body":'updated text',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog_Post.objects.last().title, 'updated title')
        self.assertEqual(Blog_Post.objects.last().body, 'updated text')
    
    def test_delete_deleteview(self):
        response = self.client.post(reverse('blog:delete_post', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        
    