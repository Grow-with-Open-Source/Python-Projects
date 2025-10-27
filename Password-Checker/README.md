# Password-Checker

Password-Checker is a simple script that checks the strength of a given password and provides suggestions to improve its security. It also suggests a better password based on the given password.

You can either provide your input as a command line argument or interactively through the terminal _(but it's always recommended to use interactive session on console)_. This is a basic script that perform minimum basic checks and suggestion. 

> [!IMPORTANT]
> Since this script serves as a foundational example, it may not be fully suitable for real-world use cases yet. However, its purpose is to establish a solid groundwork for more advanced versions. As the author, I look forward to seeing further improvements and refactoring that will enhance this script to meet real-world requirements.

## Requirements

The only requirement for running this script in your local system is Python 3.6 or above. No external dependencies are required.

## Usage

### For *unix-based systems
To use this script, run the following command:

```bash
curl -s https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Password-Checker/check-password.py | python
```

or

```bash
wget -qO- https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Password-Checker/check-password.py | python
```

or you can download the file from GitHub and then run the script by giving permission to execute the file as shown below:

```bash
# Downloading the script
wget https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Password-Checker/check-password.py

# --- OR ---
# curl -o script.py https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Password-Checker/check-password.py
# ----------

# Giving permission to execute the file
chmod +x check-password.py

# Running the script
./check-password.py
```

### For Windows

Usually, powershell in Window 10 or later version consist of `curl` binary, so you can do that same thing as shown above. But in case it doesn't work, you can use the following command:

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/Grow-with-Open-Source/Python-Projects/main/Password-Checker/check-password.py -OutFile "$env:TEMP\temp_script.py"
python "$env:TEMP\temp_script.py"
```

If you want to save the script for later usage, then it's best recommended to download the script in a desired location and run the script using python interpreter.

## Contributing

Please make sure you have used it this script before you start contributing, and then please go through the [Contributing Guidelines](https://github.com/Grow-with-Open-Source/Python-Projects/blob/main/CONTRIBUTING.md) to make your contribution.

> [!NOTE]
> Since this mini-project was meant to be a sample groundwork for more advancements, add your changes and contributions into the following [Change Log](#change-log) in the given format.

## Change Log

- PR [#37](https://github.com/Grow-with-Open-Source/Python-Projects/pull/37): Created the basic script with minimum features.

## License

This project is released under the [Apache License 2.0](https://github.com/Grow-with-Open-Source/Python-Projects/blob/main/LICENSE).