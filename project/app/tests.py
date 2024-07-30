from django.test import TestCase
from django.urls import reverse

from hashlib import md5
import json


class ChatTests(TestCase):
    CSRF_TOKEN = md5('test'.encode()).hexdigest()
    CHAT_URL = reverse('app:chat')

    def set_csrf_token(self):
        self.client.cookies['csrftoken'] = self.CSRF_TOKEN

    def test_get_method(self):
        self.set_csrf_token()
        response = self.client.get(self.CHAT_URL)
        self.assertEqual(response.status_code, 200)

    def test_post_method(self):
        self.set_csrf_token()
        response = self.client.post(self.CHAT_URL)

        # Method Does Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_put_method(self):
        self.set_csrf_token()
        response = self.client.put(self.CHAT_URL)

        # Method Does Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_patch_method(self):
        self.set_csrf_token()
        response = self.client.patch(self.CHAT_URL)

        # Method Does Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_delete_method(self):
        self.set_csrf_token()
        response = self.client.delete(self.CHAT_URL)

        # Method Does Not Allowed
        self.assertEqual(response.status_code, 405)


class LLMAPITests(TestCase):
    CSRF_TOKEN = md5('test'.encode()).hexdigest()
    LLM_API_URL = reverse('app:llm_api')

    def set_csrf_token(self):
        self.client.cookies['csrftoken'] = self.CSRF_TOKEN
        self.client.json_encoder = True

    def test_post_method(self):
        self.set_csrf_token()
        response = self.client.post(
            self.LLM_API_URL,
            data=json.dumps({
                'history': [{
                    'role': 'user',
                    'content': 'Who are you?',
                }]
            }),
            content_type='application/json',
        )
        response_body = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertIsNot(response_body, None)
        self.assertIsNot(response_body.get('answer'), None)

    def test_get_method(self):
        self.set_csrf_token()
        response = self.client.get(self.LLM_API_URL)

        # Method Does Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_put_method(self):
        self.set_csrf_token()
        response = self.client.put(self.LLM_API_URL)

        # Method Does Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_patch_method(self):
        self.set_csrf_token()
        response = self.client.patch(self.LLM_API_URL)

        # Method Does Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_delete_method(self):
        self.set_csrf_token()
        response = self.client.delete(self.LLM_API_URL)

        # Method Does Not Allowed
        self.assertEqual(response.status_code, 405)
