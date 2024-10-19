#!/usr/bin/env python

import os
import json

'''
This script requires following environment variables:

- REPO_NAME:
  > example: 'iamwatchdogs/test'
  > GitHub action variable: ${{ github.repository }}
'''


def find_table_points(lines):
	"""
	Find table points within a given list of lines.

	The table points are determined by the presence of the markers:
		<!-- TABLE BEGINS -->
		<!-- TABLE ENDS -->

	Args:
		lines (list): List of lines to search in.

	Returns:
		tuple: A tuple of two integers containing the start and end indices of
			the table points.

	Raises:
		SystemExit: If the table markers are not found or if the table end
			marker appears before the table start marker.
	"""

	# Setting default return values
	table_start = None
	table_end = None

	# Setting the markers
	table_start_marker = '<!-- TABLE BEGINS -->'
	table_end_marker = '<!-- TABLE ENDS -->'

	# Iterating over lines to find the markers
	for index, line in enumerate(lines):
		if table_start is None and table_start_marker in line:
			table_start = index
		elif table_end is None and table_end_marker in line:
			table_end = index
		if table_start is not None and table_end is not None:
			break

	# Checking for possible errors
	if table_start is None or table_end is None:
		print('Table not found in the file.')
		exit(1)
	elif table_start >= table_end:
		print('Invaild use of table markers.')
		exit(2)

	return (table_start, table_end)


def main():
	"""
	Update the index.md file with the latest contributors data.

	This function retrieves the REPO_NAME environment variable and the
	CONTRIBUTORS_LOG file path. It then reads the log file and extracts the
	data from it. The function then reads the index.md file and calculates
	the table points. If the table does not exist, it creates the table
	header. The function then iterates over the log data and updates the
	table with the latest data. Finally, it updates the index.md file with
	the updated data and prints a success message.

	"""

	# Retrieving Environmental variables
	REPO_NAME = os.environ.get('REPO_NAME')

	# Setting path for the log JSON file
	TARGET_FILE = 'index.md'
	CONTRIBUTORS_LOG = '.github/data/contributors-log.json'

	# Retrieving data from log file
	with open(CONTRIBUTORS_LOG, 'r') as json_file:
		data = json.load(json_file)

	# Reading lines from the file
	with open(TARGET_FILE, 'r') as file:
		lines = file.readlines()

	# Calculating Stating and ending points of the targeted table
	table_start, table_end = find_table_points(lines)

	# Creating table header if doesn't exist
	if table_end - table_start == 1:
		table_header = list()
		table_header.append(
			'| Project Title | Contributor Names | Pull Requests | Demo |\n')
		table_header.append('| --- | --- | --- | --- |\n')
		lines[table_start+1:table_end] = table_header

	# Initializing empty list for lines
	updated_lines = list()

	# Iterating over log to update target file
	for title, details in data.items():

		# Processing contributors-names
		contributors_names = details['contributor-name']
		contributors_names_list = [
			f'[{name}](https://github.com/{name} "goto {name} profile")' for name in contributors_names]
		contributors_names_output = ', '.join(contributors_names_list)

		# Processing pull-requests
		pull_requests = details['pull-request-number']
		pull_requests_list = [
			f'[#{pr}](https://github.com/{REPO_NAME}/pull/{pr} "visit pr \#{pr}")' for pr in pull_requests]
		pull_requests_output = ', '.join(pull_requests_list)

		# Processing demo-path
		demo_path = details['demo-path']
		if ' ' in demo_path:
			demo_path = '%20'.join(demo_path.split())
		demo_path_output = f'[/{REPO_NAME}/{title}/]({demo_path} "view the result of {title}")'
		if title == 'root' or title == '{init}':
			demo_path_output = f'[/{REPO_NAME}/]({demo_path} "view the result of {title}")'
		elif title == '{workflows}':
			demo_path_output = f'[/{REPO_NAME}/.github/workflows]({demo_path} "view the result of {title}")'
		elif title == '{scripts}':
			demo_path_output = f'[/{REPO_NAME}/.github/scripts]({demo_path} "view the result of {title}")'
		elif title == '{others}':
			demo_path_output = f'[/{REPO_NAME}/.github]({demo_path} "view the result of {title}")'

		# Appending all data together
		updated_lines.append(
			f'| {title} | {contributors_names_output} | {pull_requests_output} | {demo_path_output} |\n')

	# Updating the lines with updated data
	lines[table_start+3:table_end] = updated_lines

	# Updating the target file
	with open(TARGET_FILE, 'w') as file:
		file.writelines(lines)

	# Printing Success Message
	print(f"Updated '{TARGET_FILE}' Successfully")


if __name__ == '__main__':
	main()
