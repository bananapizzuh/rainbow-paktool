# PAKLIB
A library/cli written in python to use with the Rainbow Studios .pak files found in their games. Please report any issues found, or feel free to submit a pull request.

## Installation
`pip install git+https://github.com/bananapizzuh/paklib.git`

## Usage

### Cli
`pak-cli decompile <input_file.pak> <output_directory>` 
or
`pak-cli compile <directory_path> <output_file.pak>`

### Library
```py 
import paklib

paklib.decompile_file('input.pak', 'path/to/output_directory')
```
or
```py
import paklib

paklib.compile_directory('path/to/directory', 'output.pak')
```