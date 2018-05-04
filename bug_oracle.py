#!/usr/bin/python


import sys
import os
import requests
import json
import datetime
import re
from time import sleep
from requests.auth import HTTPBasicAuth
#import pexpect
import logging
import subprocess
from logging.handlers import RotatingFileHandler

# Initialize the application logger 
logger = logging.getLogger("Bug Oracle Log")
logger.setLevel(logging.INFO)

# Constants used by program
issue_id = ''
JIRA_URL = 'https://jira.edgewaternetworks.com/rest/api/2/issue/'
JIRA_USER = 'tp_ci@edgewaternetworks.com'
JIRA_PASSWORD = 'ewn@123'
JIRA_LINK = 'https://jira.edgewaternetworks.com'

def bugOracle(key):
	#jira_id = str(sys.argv[1])

	jira_id = key
	pattern  = ur"displayId"
	display_id = []

	# Check connectivity to JIRA
	try:
		cmd = 'curl -IsSf '+JIRA_LINK
		subprocess.check_output(cmd, shell=True,stderr=subprocess.STDOUT)
	except subprocess.CalledProcessError as e:
		print "Terminating the script due to loss of connection to JIRA"
		raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
		exit()

	response = requests.get(JIRA_URL + jira_id,auth=HTTPBasicAuth(JIRA_USER,JIRA_PASSWORD))
	get_response = json.loads(response.text)
	issue_id = get_response['id']
	logger.info('\n' + "Issue id of Bug "+issue_id)
	JIRA_URL_GET_COMMITS = 'https://jira.edgewaternetworks.com/rest/dev-status/1.0/issue/detail?issueId='+issue_id+'&applicationType=stash&dataType=repository'
	commits_response = requests.get(JIRA_URL_GET_COMMITS,auth=HTTPBasicAuth(JIRA_USER,JIRA_PASSWORD))
	json_response = json.loads(commits_response.text)
	string_json = str(json_response)

	ids = re.findall(pattern, string_json)

	for i in range(len(ids)):
		display_id.append(json_response['detail'][0]['repositories'][0]['commits'][i]['displayId'])


	path = "/home/pvincent/git/e30"
	os.chdir(path)
	cmd2 = "cd " + path +"; git pull"
	print "** Running command'" + cmd2 + "'"
	os.popen(cmd2).read()
	cmd1  = "git branch --contains "+ display_id[-1]+" -a | grep 'remotes/origin' | egrep '/master|/ver.*br' | grep -v '/HEAD'"
	print "** Running command '" + cmd1 + "'"
	result = os.popen(cmd1).read()
	print type(result)
	res = result.split('\n')
	print res
	res = list(filter(None, res))
	thelist = []
	for i in res:
		i = str(i)
		b=i.split("/")
		print b
		thelist.append(b[2])
	print thelist	

	with open('/tmp/bug_oracle_versions.txt', 'w') as f:
		for item in thelist:
			print item
			f.write(item + "\n")
	return thelist

#versions = bugOracle()
#print versions
