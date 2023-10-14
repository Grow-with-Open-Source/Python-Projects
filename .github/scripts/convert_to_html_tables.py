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

	# Creating HTML table header to replace md table
	table_header = list()
	table_header.append('<table>\n')
	table_header.append('\t<tr align="center">\n')
	table_header.append('\t\t<th>Project Title</th>\n')
	table_header.append('\t\t<th>Contributor Names</th>\n')
	table_header.append('\t\t<th>Pull Requests</th>\n')
	table_header.append('\t\t<th>Demo</th>\n')
	table_header.append('\t</tr>\n')

	# Initializing empty list for lines
	updated_lines = list()

	# Iterating over log to update target file
	for title, details in data.items():

		# Processing contributors-names
		contributors_names = details['contributor-name']
		contributors_names_list = [f'<a href="https://github.com/{name}" title="goto {name} profile">{name}</a>' for name in contributors_names]
		contributors_names_output = ', '.join(contributors_names_list)

		# Processing pull-requests
		pull_requests = details['pull-request-number']
		pull_requests_list = [f'<a href="https://github.com/{REPO_NAME}/pull/{pr}" title="visit pr \#{pr}">{pr}</a>' for pr in pull_requests]
		pull_requests_output = ', '.join(pull_requests_list)

		# Processing demo-path
		demo_path = details['demo-path']
		if ' ' in demo_path:
			demo_path = '%20'.join(demo_path.split())
		demo_path_output = f'<a href="{demo_path}" title="view the result of {title}">/{REPO_NAME}/{title}/</a>'

		# Appending all data together
		updated_lines.append('\t<tr align="center">\n')
		updated_lines.append(f'\t\t<td>{title}</td>\n')
		updated_lines.append(f'\t\t<td>{contributors_names_output}</td>\n')
		updated_lines.append(f'\t\t<td>{pull_requests_output}</td>\n')
		updated_lines.append(f'\t\t<td>{demo_path_output}</td>\n')
		updated_lines.append(f'\t</tr>\n')

	# Table footer
	table_footer = ['</table>\n']

	# Updating the lines with updated data
	lines[table_start+1:table_end] = table_header+updated_lines+table_footer

	# Updating the target file
	with open(TARGET_FILE, 'w') as file:
		file.writelines(lines)

	# Printing Success Message
	print(f"Updated '{TARGET_FILE}' Successfully")


if __name__ == '__main__':
	main()