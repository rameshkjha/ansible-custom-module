#!/usr/bin/python


DOCUMENTATION = '''
---
module: test_module

short_description: This will record client machine name where playbook ran.

options:
  None
'''

EXAMPLES = '''
- name: record remote host
- record_remote_host: remotehost="{{ inventory_hostname }}"
'''

from ansible.module_utils.basic import AnsibleModule
from datetime import datetime
import json
import sys
import os.path
import fileinput, re
import socket
from os import path

filename = "log.json"

_FILENAME_CFG="filename.cfg"

unqfilename = socket.gethostname()+datetime.now().strftime("%Y%m%d%H%M%S")+".json"

id = unqfilename[:-5]

def main():
 module = AnsibleModule(
    argument_spec=dict({})
 )


 data = dict(
    output="playbook log file created, id stored successfully",
 )
 try:
     with open(unqfilename, 'w') as outfile:
         outfile.write("{")
         outfile.write('\n')
         outfile.write("\"id\"" + ": " + '"{}"'.format(id))
         outfile.write("}")
         outfile.close()

         with open(_FILENAME_CFG, 'w') as file:
             file.write("filename=" + unqfilename)
             file.close()

 except Exception as e:
     module.fail_json(msg='Error in generate-playbook-log')

 module.exit_json(changed=True, success=data, msg=unqfilename)


if __name__ == '__main__':
    main()
