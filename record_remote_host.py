#!/usr/bin/python


DOCUMENTATION = '''
---
module: record_remote_host

short_description: This will record remote hostname where playbook ran.

description:
    - "This module will record all the hosts from inventory where playbook was run"

options:
    remotehost:
        description:
            - remotehost name passed as parameter while calling this module
        required: true
'''

EXAMPLES = '''
- name: record remote host
- record_remote_host: remotehost="{{ inventory_hostname }}"
'''


from ansible.module_utils.basic import AnsibleModule
import json
import sys
import os.path
import fileinput, re
import socket
from os import path

_FILENAME_CFG = "filename.cfg"

def read_cfg():
    try:
        cfgfile = file(_FILENAME_CFG)
        for line in cfgfile:
            if "filename=" in line:
                name, value = line.split("=", 1)
                return value
                break

    except Exception as e:
        module.fail_json(msg='Error read_cfg')


filename = read_cfg()

""" check string i.e. run-on already in file """
def check_string():
    try:
        datafile = file(filename)
        for line in datafile:
            if "run-on" in line:
                return True
                datafile.close()
                break

    except Exception as e:
        module.fail_json(msg='Error string_check')


def main():
 module = AnsibleModule(
    argument_spec = dict(
        remotehost = dict(required=True, type='str'),
    )
 )

 remotehost = module.params['remotehost']

 data = dict(
    output="remotehost stored successfuly",
 )


 try:
    if os.path.exists(filename):  # open file to append
        if check_string():
            with open(filename, 'r') as file:
                file_data = file.read()
                upd_data = file_data.replace(']', ',' + '"{}"'.format(remotehost) + "]")
            with open(filename, 'w') as file:
                file.write(upd_data)
                file.close()
        else:
            with open(filename, 'a') as outfile:
                outfile.seek(-1, os.SEEK_END)
                print("after SEEK")
                outfile.truncate()
                outfile.write(',')
                outfile.write('\n')
                outfile.write("\"run-on\"" + ": [" + '"{}"'.format(remotehost))
                outfile.write("]")
                outfile.write("}")
                outfile.close()

    else:  # create a new file
        with open(filename, 'w') as outfile:
            outfile.write("{")
            outfile.write('\n')
            outfile.write("\"run-on\"" + ": [" + '"{}"'.format(remotehost))
            outfile.write("]")
            outfile.write("}")
            outfile.close()

 except Exception as ex:
    module.fail_json(msg='Error in record-remote-host')
 module.exit_json(changed=True, success=data, msg=data)

if __name__ == '__main__':
    main()
