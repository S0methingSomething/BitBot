
import unittest
from unittest.mock import patch
from src import helpers

class TestHelpers(unittest.TestCase):

    @patch('pathlib.Path.read_text', return_value='key = "value"')
    def test_load_config(self, mock_read_text):
        with patch('toml.loads', return_value={'key': 'value'}):
            config = helpers.load_config()
            self.assertEqual(config, {'key': 'value'})

    @patch('pathlib.Path.read_text', return_value='{}')
    def test_load_bot_state(self, mock_read_text):
        with patch('json.loads', return_value={}):
            state = helpers.load_bot_state()
            self.assertEqual(state, {'online': {'last_posted_versions': {}}, 'offline': {'last_generated_versions': {}}})

    @patch('pathlib.Path.write_text')
    def test_save_bot_state(self, mock_write_text):
        with patch('json.dumps', return_value='{"key": "value"}') as mock_dumps:
            helpers.save_bot_state({'key': 'value'})
            mock_dumps.assert_called_once_with({'key': 'value'}, indent=2)
            mock_write_text.assert_called_once_with('{"key": "value"}')

    @patch('pathlib.Path.read_text', return_value='[1, 2, 3]')
    def test_load_release_state(self, mock_read_text):
        with patch('json.loads', return_value=[1, 2, 3]):
            state = helpers.load_release_state()
            self.assertEqual(state, [1, 2, 3])

    @patch('pathlib.Path.write_text')
    def test_save_release_state(self, mock_write_text):
        with patch('json.dumps', return_value='[1, 2, 3]') as mock_dumps:
            helpers.save_release_state([1, 2, 3])
            mock_dumps.assert_called_once_with([1, 2, 3], indent=2)
            mock_write_text.assert_called_once_with('[1, 2, 3]')

    def test_parse_release_notes_structured(self):
        body = "app: test_app\nversion: 1.2.3\nasset_name: test_asset.zip"
        config = {'apps': [{'id': 'test_app', 'displayName': 'Test App'}], 'github': {'assetFileName': 'test_asset.zip'}}
        result = helpers.parse_release_notes(body, "", "", config)
        self.assertEqual(result, {'app_id': 'test_app', 'display_name': 'Test App', 'version': '1.2.3', 'asset_name': 'test_asset.zip'})

    def test_parse_release_notes_legacy_tag(self):
        tag_name = "test_app-v1.2.3"
        config = {'apps': [{'id': 'test_app', 'displayName': 'Test App'}], 'github': {'assetFileName': 'test_asset.zip'}}
        result = helpers.parse_release_notes("", tag_name, "", config)
        self.assertEqual(result, {'app_id': 'test_app', 'display_name': 'Test App', 'version': '1.2.3', 'asset_name': 'test_asset.zip'})

    def test_parse_release_notes_legacy_title(self):
        title = "Test App v1.2.3"
        config = {'apps': [{'id': 'test_app', 'displayName': 'Test App'}], 'github': {'assetFileName': 'test_asset.zip'}}
        result = helpers.parse_release_notes("", "", title, config)
        self.assertEqual(result, {'app_id': 'test_app', 'display_name': 'Test App', 'version': '1.2.3', 'asset_name': 'test_asset.zip'})

    def test_parse_release_notes_bitlife(self):
        tag_name = "1.2.3"
        config = {'apps': [{'id': 'bitlife', 'displayName': 'BitLife'}], 'github': {'assetFileName': 'test_asset.zip'}}
        result = helpers.parse_release_notes("", tag_name, "", config)
        self.assertEqual(result, {'app_id': 'bitlife', 'display_name': 'BitLife', 'version': '1.2.3', 'asset_name': 'test_asset.zip'})

    def test_parse_release_notes_no_match(self):
        config = {'apps': [], 'github': {'assetFileName': 'test_asset.zip'}}
        result = helpers.parse_release_notes("", "", "", config)
        self.assertIsNone(result)

    def test_parse_versions_from_post_changelog(self):
        post = unittest.mock.Mock()
        post.selftext = "## Changelog\n- Test App updated to version 1.2.3"
        config = {'apps': [{'id': 'test_app', 'displayName': 'Test App'}]}
        result = helpers.parse_versions_from_post(post, config)
        self.assertEqual(result, {'test_app': '1.2.3'})

    def test_parse_versions_from_post_legacy_title(self):
        post = unittest.mock.Mock()
        post.selftext = ""
        post.title = "New version for Test App v1.2.3"
        config = {'apps': [{'id': 'test_app', 'displayName': 'Test App'}]}
        result = helpers.parse_versions_from_post(post, config)
        self.assertEqual(result, {'test_app': '1.2.3'})

    def test_parse_versions_from_post_no_match(self):
        post = unittest.mock.Mock()
        post.selftext = ""
        post.title = ""
        config = {'apps': []}
        result = helpers.parse_versions_from_post(post, config)
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()
