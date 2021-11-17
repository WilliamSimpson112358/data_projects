from __future__ import print_function
import jenkins
import user_details as ud
import user_env as ue
import time
import json
import requests
import sys

inv = ue.my_inv
schema = ue.my_schema
token = ue.my_token

jenkins_url = 'http://jenkins-url/'
jenkins_queue = 'http://jenkins-url/queue/api/xml'
schema_create_job = 'http://jenkins-url/job-name'

server = jenkins.Jenkins(schema_create_job, username=ud.user_name(), password=token)

def get_build_numer():
  next_build_numb = server.get_job_info('NAMEOFJOB')['nextBuildNumber']
  
def create_schema():
  params = {'':'', '':''}
  server.build_job('NAMEOFJOB', params, token=token)
  
def check_build_status(build_number):
  schema_name = check_schema_matches(build_number)
  if schema_name != schema:
    print('nno matches')
  else:
    was_built = poll_build_status(build_number)
    return was_built
    
def poll_build_status(build_number):
  building = server.get_build_info('NAMEOFJOB', build_number)["building"]
  count = 0
  
  while building:
    print(Currently Building:', building, 'and build time:', count, "seconds", end="\r")
    count += 5
    sys.stdout.flush()
    time.sleep(5)
    poll = server.get_build_info('NAMEOFJOB', build_number)["building"]
    building = poll
  return building
  
def check_schema_matches(build_number):
  build_info = server.get_build_info('NAMEOFJOB', build_number)
  schema_name = build_info["actions"][0]["parameters"][1]["value"]
  return schema_name
  
def schema_create_job():
  print('Starting Job')
  bn = get_build_number()
  create_schema()
  time.sleep(10)
  is_building = check_build_status(bn)
  if is_building:
    return False
  else:
    return True
  
