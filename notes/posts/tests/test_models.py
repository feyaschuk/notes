from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Post

User = get_user_model()


class PostModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')

        cls.post = Post.objects.create(
            text='Текстпостатекстпостатекстпостатекстпостатекстпоста',
            title ='Заголовок',
            pub_date=None,
            author=cls.user)

    def test_text_label(self):
        """verbose_name поля text совпадает с ожидаемым."""
        post = PostModelTest.post
        verbose = post._meta.get_field('text').verbose_name
        self.assertEqual(verbose, 'Текст поста')

    def test_object_name_is_title_field(self):
        """__str__  post - это строчка с содержимым post.text

        не более 15 знаков.
        """
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))
