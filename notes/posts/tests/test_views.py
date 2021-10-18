import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post

POSTS_PER_FIRST_PAGE = 10
User = get_user_model()


class BaseTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='CatMax')
        
        cls.post = Post.objects.create(
            text='Проверяем доступность страниц профайла и отдельного поста',
            title ='Заголовок',
            author=cls.user,            
        )
        


class PostPagesTests(BaseTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        reverse_templates_names = {
            reverse('index'): 'index.html',            
            reverse('new_post'): 'new.html',
            (reverse(
                'profile', kwargs={'username': 'CatMax'})): 'profile.html',
            (reverse('post', kwargs={'username': 'CatMax',
                                     'post_id': 1})): 'post.html',
            (reverse('post_edit', kwargs={'username': 'CatMax',
                                          'post_id': 1})): 'new.html'}
        for reverse_name, template in reverse_templates_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    
    def test_profile_page_shows_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('profile', kwargs={'username': 'CatMax'}))
        some_post = response.context.get('page').object_list[0]
        self.assertEqual(some_post, self.post)

    def test_post_page_shows_correct_context(self):
        """Шаблон post сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('post', kwargs={'username': 'CatMax', 'post_id': 1}))
        some_post = response.context.get('post')
        self.assertEqual(some_post, self.post)

    def test_new_post_page_shows_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        form_data = {
            'text': 'Тестовый пост',
            'title': "Заголовок",
        }
        self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        post = Post.objects.first()
        self.assertEqual(post.text, form_data['text'])
    

    def test_post_edit_page_shows_correct_context(self):
        post = Post.objects.first()
        """При редактировании поста изменяется запись в базе данных."""
        form_data = {'text': 'Измененный тестовый пост', 'title': "Заголовок",}
        self.authorized_client.post(reverse(
            'post_edit', kwargs={'username': self.user.username,
                                 'post_id': post.id}),
            data=form_data, follow=True)
        self.assertEqual(Post.objects.get(
            text='Измененный тестовый пост'), post)



class PostImageTests(BaseTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostImageTests.user)

    def test_post_get_correct_context_with_image(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        """Валидная форма создает запись в Post."""
        form_data = {
            'text': 'Тестовый пост',
            'image': uploaded,
            'title': "Заголовок",
        }

        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        post = Post.objects.get(text='Тестовый пост')
        reverse_names = {
            reverse('index'): 'page',            
            (reverse(
                'profile', kwargs={'username': 'CatMax'})): 'page',
            (reverse('post', kwargs={'username': 'CatMax',
                                     'post_id': post.id})): 'post', }

        for reverse_name, name in reverse_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                if name == 'post':
                    post = response.context.get(name)
                else:
                    post = response.context.get(name).object_list[0]
                post_text_0 = post.text
                post_image_0 = post.image.name
                self.assertEqual(post_text_0, 'Тестовый пост')
                self.assertEqual(post_image_0, 'posts/small.gif')





    
