from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Post, Comment


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser', password='testpass123')
        cls.post = Post.objects.create(title='A test title', content='Test content', author=cls.user)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A test title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.content}', 'Test content')

    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser', password='testpass123')
        cls.post = Post.objects.create(title='A test title', content='Test content', author=cls.user)
        cls.comment = Comment.objects.create(content='Test comment content', author=cls.user, post=cls.post)

    def test_comment_content(self):
        self.assertEqual(f'{self.comment.content}', 'Test comment content')
        self.assertEqual(f'{self.comment.author}', 'testuser')
        self.assertEqual(f'{self.comment.post.title}', 'A test title')
        self.assertEqual(f'{self.comment.post.author}', 'testuser')


class BlogTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )
        self.client.force_login(self.user)
        self.post = Post.objects.create(
            title='A good title',
            content='Nice content',
            author=self.user,
        )

    def test_create_post(self):
        response = self.client.post(reverse('posts:create_post'), {
            'title': 'A good title',
            'content': 'Nice content',
            'author': self.user.id,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'A good title')

    def test_post_detail(self):
        response = self.client.get(reverse('posts:post_detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_add_comment_to_post(self):
        response = self.client.post(reverse('posts:add_comment_to_post', args=[str(self.post.id)]), {
            'content': 'A good comment',
            'author': self.user.id,
            'post': self.post.id,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.last().content, 'A good comment')
