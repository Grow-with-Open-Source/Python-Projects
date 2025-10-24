# Temp-Cleaner

Temp-Cleaner is a Python script that automates the manual process of cleaning temporary files from system temp directories. This script is compatable with major operating systems including Linux, Windows, and macOS.

This script include a good logging system that can be used to track the progress of the script. The script also comprises a command line interface that can be used to control the script from the command line to manipulate the logging mechanism.

## Requirements

The only requirement for running this script in your local system is Python 3.10 or above. No external dependencies are required.

## Usage

### For *unix-based systems
To use this script, run the following command:

```bash
curl -s https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Temp-Cleaner/temp-cleaner.py | python
```

or

```bash
wget -qO- https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Temp-Cleaner/temp-cleaner.py | python
```

or you can download the file from GitHub and then run the script by giving permission to execute the file as shown below:

```bash
# Downloading the script
wget https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Temp-Cleaner/temp-cleaner.py

# --- OR ---
# curl -o script.py https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Temp-Cleaner/temp-cleaner.py
# ----------

# Giving permission to execute the file
chmod +x temp-cleaner.py

# Running the script
./temp-cleaner.py
```

### For Windows

Usually, powershell in Window 10 or later version consist of `curl` binary, so you can do that same thing as shown above. But in case it doesn't work, you can use the following command:

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Temp-Cleaner/temp-cleaner.py -OutFile "$env:TEMP\temp_script.py"
python "$env:TEMP\temp_script.py"
```

If you want to save the script for later usage, then it's best recommended to download the script in a desired location and run the script using python interpreter.

### Command Line Arguments

If you execute the script without any arguments or options, then it will be equivalent to the following command:

```bash
./temp-cleaner.py --log-level INFO
```

Which mean, the logs will be displayed only to the console and is not stored anywhere. But you can change the logging behavior by using command line arguments/options as shown below:

```bash
usage: temp-cleaner.py [-h] [--log-level LOG_LEVEL] [--save-log] [--log-filename LOG_FILENAME] [--silent]

Temp Files Cleaner that cleans temporary files from system temp directories.

options:
  -h, --help                    show this help message and exit
  --log-level LOG_LEVEL         Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  --save-log                    Save log to a file
  --log-filename LOG_FILENAME   Specify log filename
  --silent                      Show only the progress without logging details
```

Here are more details on the options:

- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) sets the logging level for the script. **Default is `INFO`**.
- `--save-log`: Save log to a file with file name as `temp_cleaner_YYYYMMDD_HHMMSS.log`. **Default is `False`**.
- `--log-filename`: If you want to save the log file with a custom name, then you can use this option. **Default is `None`**.
- `--silent`: Displays only the progress without logging details. **Default is `False`**.

> [!IMPORTANT]
> If you're using `--silent` option, then the log file will not be saved even if you specified `--save-log` or `--log-filename` option and all the logging level will be ignored.

## Contributing

Please make sure you have used it this script before you start contributing, and then please go through the [Contributing Guidelines](https://github.com/Grow-with-Open-Source/Python-Projects/blob/main/CONTRIBUTING.md) to make your contribution.

## License

This project is released under the [Apache License 2.0](https://github.com/Grow-with-Open-Source/Python-Projects/blob/main/LICENSE).