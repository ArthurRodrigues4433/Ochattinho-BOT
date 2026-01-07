import unittest
import json
import os
import settings

class TestSettings(unittest.TestCase):
    def setUp(self):
        # Backup original settings
        self.original_prefixes = settings.PREFIXES.copy()
        self.original_log_channels = settings.LOG_CHANNELS.copy()
        self.original_mod_roles = settings.MOD_ROLES.copy()

    def tearDown(self):
        # Restore
        settings.PREFIXES = self.original_prefixes
        settings.LOG_CHANNELS = self.original_log_channels
        settings.MOD_ROLES = self.original_mod_roles
        # Remove test file if exists
        if os.path.exists('test_settings.json'):
            os.remove('test_settings.json')

    def test_save_and_load(self):
        # Modify settings
        settings.PREFIXES[123] = '!'
        settings.LOG_CHANNELS[123] = 456
        settings.MOD_ROLES[123] = 789

        # Save
        original_save = settings.save_settings
        settings.save_settings = lambda: settings._save_to_file('test_settings.json')
        settings.save_settings()
        settings.save_settings = original_save

        # Load
        original_load = settings.load_settings
        settings.load_settings = lambda: settings._load_from_file('test_settings.json')
        settings.load_settings()
        settings.load_settings = original_load

        # Check
        self.assertEqual(settings.PREFIXES[123], '!')
        self.assertEqual(settings.LOG_CHANNELS[123], 456)
        self.assertEqual(settings.MOD_ROLES[123], 789)

if __name__ == '__main__':
    unittest.main()