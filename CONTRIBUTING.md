# Welcome to CONTRIBUTING.md

Hey there, fellow Developer !!!... I'm happy to see you being hyped about making your *(probably first)* open-source contribution to this repo. We heartily welcome you to an amazing journey of open-source contribution. I hope you have fun learning and teaching at the same time. For the **Python-Projects** repo, you'll be contributing the mini-projects that you’ve built while learning the concepts of Python.

> [!NOTE]
> You can contribute either in pure python script format *(the files that end with `.py` file extension)* or as Jupyter Notebooks *(the files that end with `.ipynb` file extension)*. either of those files are accepted, so no need to convert the Jupyter Notebooks into python scripts for the sake of contribution.

## Setting up Environment

You don't need any special dependencies to use it locally, Just make sure you have *[**git**](https://git-scm.com/ "visit official website") installed in your system and [*conda enivironment*](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html "visit official website") *(depending on requirement)*. It's recommended that GitHub cli *(or)* [**gh**](https://cli.github.com/ "visit official website") is installed for easier access to your repo, but that's totally optional.

## Getting Started with Contribution

So, before you jump right into your code editor and start working on your project, make sure you understand and follow the file structure and guidelines which are mentioned below.

### Instructions and Guidelines

- Most of the time you'll be working on Python rather than the default files present within the repo. So, Make sure you **do not add/remove/modify any content present with the default files**.

  > [!IMPORTANT] 
  > - If any such changes are to be found within your Pull Request *(PR)*, then it will be **rejected** i.e., until and unless it's mentioned on an [Issue](https://github.com/Grow-with-Open-Source/Python-Projects/issues "goto issues tab").
  > - If you wish to work on default file *(either to update or fix a bug)*, create an issue first and get assigned to the issue to let others know that  the issue has been recorded and you've already begun working on it.

- Also, your Python code will be linted automatically as soon as you make the PR. The PR will be merged if and only if all the checks are completed. If there's any issue with the linting of your work, you can contact the maintainer within the conversation tab of your PR.

#### File Structure

- The basic file structure of this repo *(excluding any contributions)* as follows:

  > ```
  > /Python-Projects/
  > |
  > ├── .github
  > |       ├── data
  > |       |   └── contributors-log.json
  > |       ├── scripts
  > |       |   ├── convert_to_html_tables.py
  > |       |   ├── update_contributors_log.py
  > |       |   └── update_index_md.py
  > |       └── workflows
  > |           ├── python-linter.yml
  > |           ├── deploy-gh-pages.yml
  > |           └── update-contributors-details.yml
  > ├── _includes
  > |       └── head-custom.html
  > ├── assets
  > |       └── img
  > |           ├── page-cover.png
  > |           └── favicon.icon
  > ├── index.md
  > ├── _config.yml
  > ├── .gitignore
  > ├── LICENSE
  > ├── CODE_OF_CONDUCT.md
  > ├── CONTRIBUTING.md
  > └── README.md
  > ```

- Before you begin with your project contribution, make sure you create a new directory *(or)* folder within the repo with your project name.

  > [!NOTE]
  > It's suggested to use any of the following naming conventions for the directory *(or)* folder:
  > 
  > | Format | Example |
  > | :---: | :---: |
  > | Separated with dashes | `/my-project-name/` |
  > | Separated with underscores | `/my_project_name/` |
  >
  > Note that you can also use spaces *(like `/my project name/`)* but it's recommended to use any of the above-mentioned naming conversions.

- You can write simple docs for your project using [markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax "visit official GitHub Markdown Docs"). You can write descriptions, add screenshots or even upload a video. **Just make sure documentation is done within files named `README.md` *(or)* `index.md`**

- Even if you're project is small, try to keep it organized by keeping related files within their directories/folders

  <details>
  <summary>Here's an sample example</summary>
  <div>
  
  ```
  /Python-Projects/
  |
  ├── <Default-files>
  └── <your-project-name>
          ├── gui
          |   └── <all-your-gui-files>
          ├── database
          |   └── <all-your-database-files>
          ├── main.py
          ├── requirements.txt  # install dependencies using pip
          ├── environment.yml   # setting up conda enviroment
          └── README.md
  ```
  
  > [!NOTE]
  > Note that this is an example to give you an idea of organizing files, no need to follow the exact pattern. You can come up with your own hierarchy based on your requirements.
  
  </div>
  </details>

### Contributing

Now that you have a basic understanding of this repo, let's talk a bit about the process of contributing...

- **Step 1:** You start you setting up the environment [*(as discussed above)*](#setting-up-environment).

- **Step 2:** Now start by [forking](https://github.com/Grow-with-Open-Source/Python-Projects/fork "let's fork the repo") the repository.

- **Step 3:** Clone the forked repository to your local machine.
  ```bash
  #cloning the repo
  git clone https://github.com/<your-github-user-name>/Python-Projects.git
  
  #entering the project directory
  cd Python-Projects
  ```

- **Step 4:** Create a new branch to work on your contribution. use the following command:
  ```bash
  # create and check out to new branch
  git checkout -b <your-project-name>
  
  # check your branch currently in
  git branch
  ```

- **Step 5:** Now go ahead and create your own directory/folder with your project name with a proper naming convention and finish your project while maintaining a [file structure](#file-structure) & following other rules [*(as discussed above)*](#instructions-and-guidelines).

- **Step 6:** Make sure you commit each and every change while working on your project parallelly, *(like one commit for creating `index.js`, another for writing a piece of code, and so on...)*. Using the following command:
  ```bash
  # tracking or staging the changes
  git add .
  
  # commiting the changes
  git commit -m "<related-short-message>
  ```

  > [!IMPORTANT]
  > Make sure to commit your each and every change with proper description

- **Step 7:** After committing all the changes and completion of your work. push your commit to your forked repo, using the following commands:
  ```bash
  # check your branch name
  git branch
  
  # push your commit to the origin repo
  git push origin <your-branch-name>
  ```

- **Step 8:** Now, create a pull request to the [original repo](https://github.com/Grow-with-Open-Source/Python-Projects). [Learn about Pull requests](https://docs.github.com/articles/using-pull-requests "official GitHub documentation")

- **Step 9:** After creating the pull request wait till the linting checks are done, if there's any issue with your Python code then the checks won't pass. And if the checks won't pass you have to fix the errors, you can check the linting workflow to know where the error occurred. If you need any help, you can contact the maintainer within the PR.

- **Step 10:** If the linting checks are done and your code passes the liniting checks, then wait for the maintainer to review your code and merge the pull request. If there's any issue with your PR, the maintainer will contact you and with the help of the maintainer you can resolve the issue, so that the maintainer merge your PR.

When the maintainer merges your PR, you have successfully made your *(probably first)* open-source contribution to showcase your learning and provide a reference to a complete newbie. Everybody can see your work and make use of it. Good job, mate !!...

## Rules and Regulations

Here are some ground rules that you need to follow:

- It's important for you to commit to each and every change. Don't just finish all of your work with a single commit. If you're a newbie, it will only be tolerated 3 times.
- Sending several pull requests for a single post is not accepted.
- Your Pull Request will not be merged, if you have modified, changed or deleted any files or content that doesn't belong to you.
- Pull Request containing any illegal, NFSW or any other content which doesn't help others in any way possible will be closed immediately.
- The Pull Request will only be merged if everything seems to be in order. You be notified if you did something wrong, and your pull request will only be merged if the notified changes are made.
