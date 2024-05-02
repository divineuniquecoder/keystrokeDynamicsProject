import json
import os

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.settings = self.load_settings()

    def load_settings(self):
        # Check if the config file exists
        if not os.path.isfile(self.config_file):
            raise FileNotFoundError(f"The configuration file {self.config_file} was not found.")
        
        # Load settings from the file
        try:
            with open(self.config_file, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error parsing the configuration file: {e}")

    def get_setting(self, setting_key):
        # Retrieve a specific setting
        return self.settings.get(setting_key)

    def set_setting(self, setting_key, setting_value):
        # Update a specific setting and save back to the file
        self.settings[setting_key] = setting_value
        try:
            with open(self.config_file, 'w') as file:
                json.dump(self.settings, file, indent=4)
        except Exception as e:
            print(f"An error occurred while writing to the configuration file: {e}")

    def reload_settings(self):
        # Reload settings from the file, useful if settings were changed externally
        self.settings = self.load_settings()
