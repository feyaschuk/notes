from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.guest_client2 = Client()
        self.user2 = User.objects.create_user(username='MaxBars')
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user2)

        self.post = Post.objects.create(
            text='Проверяем доступность страниц профайла и отдельного поста',
            title= "Заголовок",
            pub_date=None,
            author=self.user,
            id='89')

    def test_pages_urls_allowed_to_non_authorized_client(self):
        """Доступность страниц неавторизованному клиенту.

        Index, profile, post недоступна неавторизованному клиенту.
        """
        urls = {
            'index.html': '/',            
            'profile.html': '/StasBasov/',
            'post.html': '/StasBasov/89/',
        }
        for url in urls.values():
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertNotEqual(response.status_code, 200)

    def test_pages_urls_allowed_to_authorized_client(self):
        """Страница new_post, post_edit доступна авторизованному клиенту."""
        urls = {
            'new_post': '/new/',
            'post_edit': '/StasBasov/89/edit/',
        }
        for url in urls.values():
            with self.subTest():
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_post_edit_urls_not_allowed_to_non_author_authorized_client(self):
        """Недоступность страниц авторизованному клиенту, не автору.

        Страница /username/post_id/edit/ недоступна авторизованному клиенту,
        не автору.
        """
        response = self.authorized_client2.get('/StasBasov/89/edit/')
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, '/StasBasov/89/')

    def test_pages_urls_redirect_anonymous_on_admin_login(self):
        """Переадресация со страниц /new/, /username/post_id/edit/.

        Страница перенаправит анонимного клиента на страницу логина.
        """
        urls = {
            'new_post': '/new/',
            'post_edit': '/StasBasov/89/edit/', }

        for url in urls.values():
            with self.subTest():
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(
                    response, ('/auth/login/?next=' + url))

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        url_templates = {
            '/': 'index.html',            
            '/new/': 'new.html',
            '/StasBasov/89/edit/': 'new.html'}
        for url, template in url_templates.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_page_not_found(self):
        """Сервер возвращает код 404, если страница не найдена."""
        url = 'goup'
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 404)
