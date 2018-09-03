from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, login
from django.contrib.messages import get_messages 


class TestViews(TestCase):
    
    def test_get_home_page(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "accounts/index.html")
        
    def test_get_login_page(self):
        page = self.client.get("/accounts/login/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "accounts/login.html")
        
    def test_get_logout_page(self):
        page = self.client.get("/accounts/logout/")
        self.assertEqual(page.status_code, 302)
        
    def test_get_registration_page(self):
        page = self.client.get("/accounts/register/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "accounts/registration.html")
    
    def test_get_profile_page(self):
        user = User(username='test_username', email='patrick.e.doherty@gmail.com',
                    first_name = 'George', last_name='Smith')
        user.save()
        page = self.client.get("/accounts/profile/{0}/".format(user.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "accounts/profile.html")
        
        
    def test_get_profile_page_that_does_not_exist(self):
        page = self.client.get("/accounts/profile/10/")
        self.assertEqual(page.status_code, 404)
        
        
    def test_get_edit_profile_page(self):
        user = User.objects.create_user(username='username', password='password')
        response = self.client.login(username='username', password='password')
        response = self.client.get("/accounts/edit-profile/{0}/".format(user.id), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/edit_profile.html")
        
    def test_get_edit_profile_page_not_authenticated(self):
        page = self.client.get("/accounts/edit-profile/2/", follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "accounts/login.html")
        
    def test_logout_page_authenticated(self):
        User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        page = self.client.get("/accounts/logout/", follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "accounts/index.html")
        
    def test_get_login_page_authenticated(self):
        User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        page = self.client.get("/accounts/login/")
        self.assertEqual(page.status_code, 302)
        
    
           
    def test_get_registration_page_user_authenticated(self):
        User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        page = self.client.get("/accounts/register/")
        self.assertEqual(page.status_code, 302)
        
    def test_register_new_user_unique_info(self):
        page = self.client.post("/accounts/register/", {'username': 'test_username', 
                                        'email': 'email.address@gmail.com',
                                        'password1': 'beyk38cmej39',
                                        'password2': 'beyk38cmej39'}, follow=True)
        
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "accounts/index.html")
        
    def test_register_new_user_duplicate_info(self):
        user = User.objects.create_user(username='test_username', password='password', email='email.address@gmail.com')
        user.save()
        response = self.client.post("/accounts/register/", {'username': 'test_username', 
                                        'email': 'email.address@gmail.com',
                                        'password1': 'beyk38cmej39',
                                        'password2': 'beyk38cmej39'}, follow=True)
        
        
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, "accounts/registration.html")
        
    
    
    def test_edit_profile_correct_info(self):
        user = User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        response = self.client.post("/accounts/edit-profile/{0}/".format(user.id), {'location':'Strabane', 
                                                                'bio':"I'm cool"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")
        
    def test_edit_profile_missing_info(self):
        user = User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        response = self.client.post("/accounts/edit-profile/{0}/".format(user.id), {}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/edit_profile.html")
        
    def test_get_login_page_not_authenticated_correct_info(self):
        User.objects.create_user(username='username', password='password')
        response = self.client.post("/accounts/login/", {"username": "username",
                                                    "password": "password"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/index.html")
        
    def test_get_login_page_not_authenticated_not_correct_info(self):
        User.objects.create_user(username='username', password='password')
        response = self.client.post("/accounts/login/", {"username": "username",
                                                    "password": "password1"}, follow=True)
                                                    
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")