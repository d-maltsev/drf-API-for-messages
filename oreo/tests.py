from django.test import TestCase

from .models import Message


class ViewsTest(TestCase):
    """
    class for testing all views methods
    """

    @classmethod
    def setUpTestData(cls):
        """
        generate messages for test
        """

        number_of_messages = 10
        for message_num in range(number_of_messages):
            Message.objects.create(title='title %s' % message_num, body='body %s' % message_num, )

    def test_view_get_list(self):
        """
        test for retrieve list of messages
        """

        resp = self.client.get('/message/')
        self.assertEqual(resp.status_code, 200)

    def test_view_create_message(self):
        """
        test for create new message
        """

        resp = self.client.post('/message/', {"title": "123", "body": "123"})
        self.assertEqual(resp.status_code, 201)

    def test_view_get_message(self):
        """
        test for retrieve message
        """

        resp = self.client.get('/message/5/')
        self.assertEqual(resp.status_code, 200)

    def test_view_delete_message(self):
        """
        test for delete message
        """

        resp = self.client.delete('/message/5/')
        self.assertEqual(resp.status_code, 204)

    def test_view_generate_csv(self):
        """
        test for generate csv
        """

        resp = self.client.get('/generate_csv/')
        self.assertEqual(resp.status_code, 200)
