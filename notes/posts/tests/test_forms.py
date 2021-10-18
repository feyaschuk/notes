import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.test.utils import override_settings
from django.urls import reverse

from ..models import Post

User = get_user_model()


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        super().setUpClass()
        cls.user = User.objects.create_user(username='CatMax')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Рекурсивно удаляем временную после завершения тестов
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)
        
        self.post = Post.objects.create(
            text='Тестовый пост',
            title="Заголовок",
            author=PostFormTests.user, )

    def test_create_post(self):
        posts_count = Post.objects.count()
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
            'title': "Заголовок",
            'text': 'Тестовый пост',
            'image': uploaded,
        }

        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        post = Post.objects.first()
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.title, form_data['title'])
        self.assertIsNotNone(post.image)

    def test_edit_post(self):
        """Редактирование поста.

        Проверяем, что изменяется соотвествующая запись в базе данных.
        """
        form_data = {'title':"Заголовок",
                     'text': 'Измененный тестовый пост', }

        response = self.authorized_client.post(reverse(
            'post_edit', kwargs={'username': self.user.username,
                                 'post_id': self.post.id}),
            data=form_data, follow=True)

        self.assertEqual(Post.objects.get(id=self.post.id).text,
                         form_data['text'])
        self.assertRedirects(response, reverse(
            'post', kwargs={'username': self.user.username,
                            'post_id': self.post.id}))


    