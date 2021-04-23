from unittest import TestCase

from manage import db, AudioFile, app
from test_data import song_record, podcast_record, audio_book_record


class AudioFileTest(TestCase):
    """
    Test Add Audio Function
    """
    def test_add_audio_file_ok(self):
        with app.test_client() as c:
            response = c.post('/podcast', json=podcast_record)
            json_data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIn("successful", json_data['response'])

    def test_add_audio_file_not_ok(self):
        with app.test_client() as c:
            response = c.post('/invalid', json={})
            json_data = response.get_json()
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid", json_data['response'])

    # Test Get Audio Function
    def test_get_audio_file_ok(self):
        with app.test_client() as c:
            response = c.get('/song/1')
            json_data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIn("songName", json_data['response'])

        with app.test_client() as c:
            response = c.get('/podcast')
            json_data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(json_data['response'], list)

    def test_get_audio_file_not_ok(self):
        with app.test_client() as c:
            response = c.get('/song/999')
            json_data = response.get_json()
            self.assertEqual(response.status_code, 400)
            self.assertIn("not found", json_data['response'])

    # Test Update Audio Function
    def test_update_audio_file_ok(self):
        with app.test_client() as c:
            response = c.put('/song/1', json={'duration': 1100})
            json_data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIn("updated", json_data['response'])

    def test_update_audio_file_not_ok(self):
        with app.test_client() as c:
            response = c.get('/song/999')
            json_data = response.get_json()
            self.assertEqual(response.status_code, 400)
            self.assertIn("not found", json_data['response'])

        with app.test_client() as c:
            response = c.get('/invalid/999')
            json_data = response.get_json()
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid", json_data['response'])

    # Test Delete Audio Function
    def test_delte_audio_file_ok(self):
        with app.test_client() as c:
            response = c.put('/song/4')
            json_data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIn("deleted", json_data['response'])

    def test_delete_audio_file_not_ok(self):
        with app.test_client() as c:
            response = c.get('/song/999')
            json_data = response.get_json()
            self.assertEqual(response.status_code, 400)
            self.assertIn("not found", json_data['response'])