import os
import json


class ConfigLoader(dict):
    def __init__(self, path, validators):
        self.path = path
        self.validators = validators
        config = self.__load_config()
        super().__init__(config)

    def __load_config(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "rt") as config_file:
                    config = json.load(config_file)
                    invalid_keys, unexpected_keys = self.__validate_paths_json(config)
                    if len(invalid_keys) == 0:
                        if len(unexpected_keys) != 0:
                            print("[WARN] '" + self.path + "' contains unexpected config keys:" +
                                  " '" + "', '".join(unexpected_keys) + "'\n")
                        return config
                    else:
                        print("[ERROR] '" + self.path + "' contains invalid config values:")
                        print("\n".join(invalid_keys))
                        exit()
            except OSError:
                print("[ERROR] Could not open '" + self.path + "'\n")
                exit()
            except ValueError:
                print("[ERROR] '" + self.path + "' has an invalid JSON structure\n")
                exit()
        else:
            self.__create_empty_config()

    def __create_empty_config(self):
        with open(self.path, "xt") as paths_file:
            expected_keys = {}
            for key in self.validators.keys():
                expected_keys[key] = ""
            json.dump(expected_keys, paths_file, indent=4)
            print("[ERROR] Created config file '" + self.path + "', fill out before running again\n")
            exit()

    def __validate_paths_json(self, config):
        invalid_keys = []
        unexpected_keys = []
        all_keys = set(self.validators.keys()).union(set(config.keys()))
        for key in all_keys:
            validator = self.validators.get(key, None)
            if validator:
                valid, message = validator(key, config[key])
                if not valid:
                    invalid_keys.append(message)
            else:
                unexpected_keys.append(key)
        return invalid_keys, unexpected_keys

    @staticmethod
    def validate_nothing(key, value):
        return True, ""

    @staticmethod
    def validate_not_empty(key, value):
        if value == "":
            return False, f"         - '{key}' cannot be empty"
        return True, ""

    @staticmethod
    def validate_folder(key, value):
        if value == "":
            return False, f"         - '{key}' cannot be empty"
        elif not os.path.exists(value):
            return False, f"         - '{key}: {value}' does not exist"
        elif not os.path.isdir(value):
            return False, f"         - '{key}: {value}' is not a folder"
        return True, ""

    @staticmethod
    def validate_file(key, value):
        if value == "":
            return False, f"         - '{key}' cannot be empty"
        elif not os.path.exists(value):
            return False, f"         - '{key}: {value}' does not exist"
        elif not os.path.isfile(value):
            return False, f"         - '{key}: {value}' is not a file"
        return True, ""

    @staticmethod
    def validate_json_file(key, value):
        if value == "":
            return False, f"         - '{key}' cannot be empty"
        elif not os.path.exists(value):
            return False, f"         - '{key}: {value}' does not exist"
        elif not os.path.isfile(value):
            return False, f"         - '{key}: {value}' is not a file"
        else:
            try:
                with open(value, "rt", encoding="utf-8") as json_file:
                    json.load(json_file)
                    return True, ""
            except ValueError:
                return False, f"         - '{key}: {value}' is not valid JSON file"
