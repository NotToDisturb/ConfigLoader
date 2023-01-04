# ConfigLoader
ConfigLoader is a Python 3.8 package built to make loading and creating configurations a simpler process.

## Package usage
#### Installation

`pip install git+https://github.com/NotToDisturb/ConfigLoader.git#egg=ConfigLoader`
<br><br>
#### Documentation

- [`ConfigLoader`](#configloaderpath-str-validators-dict)
- [`ConfigLoader.validate_nothing`](#configloadervalidate_nothingkey-str-value-str---tuple)
- [`ConfigLoader.validate_not_empty`](#configloadervalidate_not_emptykey-str-value-str---tuple)
- [`ConfigLoader.validate_folder`](#configloadervalidate_folderkey-str-value-str---tuple)
- [`ConfigLoader.validate_file`](#configloadervalidate_filekey-str-value-str---tuple)
- [`ConfigLoader.validate_json_file`](#configloadervalidate_json_filekey-str-value-str---tuple)

<br>

> ##### `ConfigLoader(path: str, validators: dict)`
> 
> There are three possible outcomes:
> 1. If the config file doesn't exist, create it using the keys in `validators` and stop the script<br>
> 1. If the config file exists but it doesn't pass all the validators,
>        print the validators that fail and stop the script<br>
> 1. If the config file exists and it passes all the validators, create an
>        instance of ConfigLoader, which inherits from `dict`
>
> In outcomes 2 and 3, if any unexpected keys are found they will be pointed out but
> execution won't be interrupted

<br>

> ##### `ConfigLoader.validate_nothing(key: str, value: str) -> tuple`
>
> Ensures that the `key` exists in the config

<br>

> ##### `ConfigLoader.validate_not_empty(key: str, value: str) -> tuple`
>
> Validates if the `value` of `key` is not `""`

<br>

> ##### `ConfigLoader.validate_folder(key: str, value: str) -> tuple`
>
> Validates if the `value` of `key` is a path that exists and points to a folder

<br>

> ##### `ConfigLoader.validate_file(key: str, value: str) -> tuple`
>
> Validates if the `value` of `key` is a path that exists and points to a file

<br>

> ##### `ConfigLoader.validate_json_file(key: str, value: str) -> tuple`
>
> Validates if the `value` of `key` is a path that exists and points to a correct JSON file

<br>

#### Example usage
Here is an example of how to use ConfigLoader:
```
from configloader import ConfigLoader

CONFIG_JSON = "config.json"
validators = {
    "hello_world_txt": ConfigLoader.validate_file,
    "content":         ConfigLoader.validate_not_empty
}

config = ConfigLoader(CONFIG_JSON. validators)
print(config["hello_world_txt"])
```
The first time this script is run, it will exit after generating `config.json` (the path indicated in `CONFIG_JSON`).
The generated file will contain all the keys from `validators` with `""` assigned to them. Subsequent runs will continue exiting until the configuration file is filled out so that all the `validators` pass.