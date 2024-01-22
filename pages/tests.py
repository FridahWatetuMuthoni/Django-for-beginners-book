from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from .models import Post

# Create your tests here.

class PostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(text="This is a test")
    
    def test_model_content(self):
        self.assertEqual(self.post.text, 'This is a test')
    
    
    def test_url_exists_at_correct_location(self):
        response = self.client.get('/pages/')
        self.assertEqual(response.status_code, 200)
    
    def test_home_template(self):
        response = self.client.get(reverse('pages:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/home.html')
        self.assertContains(response, 'This is a test')
        


class AboutPageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get('/pages/about/')
        self.assertEqual(response.status_code, 200)
    
    def test_url_available_by_name(self):
        response = self.client.get(reverse('pages:about'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_name_correct(self):
        response = self.client.get(reverse('pages:about'))
        self.assertTemplateUsed(response, 'pages/about.html')
    
    def test_template_content(self):
        response = self.client.get(reverse('pages:about'))
        self.assertContains(response, '<h1>About Page</h1>')
