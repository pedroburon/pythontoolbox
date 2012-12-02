from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from accounts.models import Profile
from accounts.forms import ProfileForm, ChangeEmailForm


PASSWORD = 'password'


class ProfileCreateOnSignalTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(username='username')

        self.assertIsNotNone(user.get_profile())
        self.assertIsInstance(user.get_profile(), Profile)

    def test_save_user(self):
        user = User.objects.create(username='username')
        user.first_name = 'User'
        user.save()

        self.assertIsNotNone(user.get_profile())
        self.assertIsInstance(user.get_profile(), Profile)
        self.assertEqual(1, Profile.objects.count())


class ProfileDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='username')

    def test_get_inexistent(self):
        response = self.client.get(reverse('accounts_profile_detail', kwargs={'username': 'inexistent'}))

        self.assertEqual(404, response.status_code)

    def test_get(self):
        response = self.client.get(reverse('accounts_profile_detail', kwargs={'username': self.user.username}))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'accounts/profile_detail.html')
        self.assertIn('profile', response.context)
        self.assertEqual(response.context['profile'], self.user.get_profile())

    def test_post(self):
        response = self.client.post(reverse('accounts_profile_detail', kwargs={'username': self.user.username}))

        self.assertEqual(405, response.status_code)


class ProfileUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', password=PASSWORD, email='username@example.net')

        self.url = reverse('accounts_profile_update')

    def test_get(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(self.url)

        self.assertIn('profile', response.context)
        self.assertEqual(response.context['profile'], self.user.get_profile())
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ProfileForm)

    def test_get_anonymous(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, settings.LOGIN_URL + '?next=' + self.url)


class EmailChangeViewTest(TestCase):
    def setUp(self):
        self.email = 'initial@example.net'
        self.user = User.objects.create_user(username='username', password=PASSWORD, email=self.email)
        self.url = reverse('accounts_change_email')

    def test_get(self):
        self.client.login(username=self.user.username, password=PASSWORD)

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ChangeEmailForm)
        self.assertEqual(response.context['form'].instance, self.user)
        self.assertTemplateUsed(response, 'accounts/change_email.html')

    def test_get_anonymous(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, settings.LOGIN_URL + '?next=' + self.url)

    def test_post(self):
        self.client.login(username=self.user.username, password=PASSWORD)

        response = self.client.post(self.url, {'email': 'new@example.net'})

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(mail.outbox[0].subject, 'Please confirm your new address')
        self.assertRedirects(response, reverse('accounts_change_email_sent'))

    def test_get_change_email_complete(self):
        self.client.login(username=self.user.username, password=PASSWORD)

        response = self.client.get(reverse('accounts_change_email_sent'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'accounts/change_email_sent.html')

    def test_post_existing_email(self):
        existing = User.objects.create_user(username='existing', password=PASSWORD, email='existing@example.net')
        self.client.login(username=self.user.username, password=PASSWORD)

        response = self.client.post(self.url, {'email': existing.email})

        self.assertEqual(200, response.status_code)
        self.assertFormError(response, 'form', 'email', _(u'This E-mail is already used'))

    def test_post_same_email(self):
        self.client.login(username=self.user.username, password=PASSWORD)

        response = self.client.post(self.url, {'email': self.user.email})

        self.assertEqual(200, response.status_code)
        self.assertFormError(response, 'form', 'email', _(u'This E-mail is already used'))
