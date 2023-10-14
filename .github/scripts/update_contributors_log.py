#!/usr/bin/env python

import os
import json

'''
This script requires following environment variables:

- REPO_NAME:
  > example: 'iamwatchdogs/test'
  > GitHub action variable: ${{ github.repository }}

- PR_NUMBER:
  > example: '5'
  > GitHub action variable: ${{ github.event.pull_request.number }}
'''

def get_project_title(pr_data):

	# Setting default value
	project_title = 'root'

	# Iterating through the "files" list
	for i in pr_data["files"]:
		if '/' in i["path"]:
			project_title = i["path"]
			break

	# If we find a directory
	if project_title != 'root':
		project_title = project_title.split('/')[0]

	return project_title

def get_contributor_name(pr_data):
	return pr_data["author"]["login"]

def get_demo_path(pr_data):

	# Getting required values
	REPO_NAME = os.environ.get('REPO_NAME')
	PROJECT_NAME = get_project_title(pr_data)

	# Handling a base case
	if PROJECT_NAME == 'root':
		return f'https://github.com/{REPO_NAME}/'

	# Setting default value
	demo_path = f'https://github.com/{REPO_NAME}/tree/main/{PROJECT_NAME}' 
	found_required_path = False

	# Iterating through the "files" list
	for file_data in pr_data["files"]:
		path = file_data["path"]
		if "index.html" in path:
			demo_path = path
			found_required_path = True
			break
		elif  path.lower().endswith('index.md') or path.lower().endswith('readme.md'):
			demo_path = path
			found_required_path = True

	# Modifying demo path as a route
	if found_required_path:
		demo_path = '/'.join(demo_path.split('/')[:-1])

	# Checking out for spaces:
	if ' ' in demo_path:
		demo_path = '%20'.join(demo_path.split())

	return demo_path

def main():

	# Setting required file paths
	CURRENT_PR_DETAILS_PATH = 'pr.json'
	CONTRIBUTORS_LOG_PATH = '.github/data/contributors-log.json'

	# Reading contents from the current pr
	with open(CURRENT_PR_DETAILS_PATH, 'r') as json_file:
		current_pr = json.load(json_file)

	# Getting required value for update
	PROJECT_TITLE = get_project_title(current_pr)
	CONTRIBUTOR_NAME = get_contributor_name(current_pr)
	PR_NUMBER = os.environ.get('PR_NUMBER')
	DEMO_PATH = get_demo_path(current_pr)

	# Creating a new dict objects for JSON conversion
	existing_data = None
	new_data = {
		PROJECT_TITLE: {
			"contributor-name": [CONTRIBUTOR_NAME],
			"pull-request-number": [PR_NUMBER],
			"demo-path": DEMO_PATH
		}
	}

	# Processing the data dumps
	operation_name = None
	if os.path.exists(CONTRIBUTORS_LOG_PATH):

		# Reading existing Log file
		with open(CONTRIBUTORS_LOG_PATH, 'r') as json_file:
			existing_data = json.load(json_file)

		# performing updation or addition based on `PROJECT_TITLE`
		if PROJECT_TITLE in existing_data:
			if CONTRIBUTOR_NAME not in existing_data[PROJECT_TITLE]["contributor-name"]:
				existing_data[PROJECT_TITLE]["contributor-name"].append(CONTRIBUTOR_NAME)
			if PR_NUMBER not in existing_data[PROJECT_TITLE]["pull-request-number"]:
				existing_data[PROJECT_TITLE]["pull-request-number"].append(PR_NUMBER)
			operation_name = 'Updated'
		else:
			existing_data.update(new_data)
			operation_name = 'Appended data to'
	else:
		existing_data = new_data
		operation_name = 'Created'

	# Dumping the data into log file
	with open(CONTRIBUTORS_LOG_PATH, 'w') as json_file:
		json.dump(existing_data, json_file, indent=2)

	# Output message
	print(f'Successfully {operation_name} the log file')

if __name__ == '__main__':
	main()