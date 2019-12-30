#!/usr/bin/python


DOCUMENTATION = '''
---
module: record_end_time

short_description: This will record start time when playbook started.

options:
  None
'''

EXAMPLES = '''
- name: record end time 
- record_end_time:
'''

from ansible.module_utils.basic import AnsibleModule
import json
import sys
import os.path
import fileinput, re
import socket
from os import path
from datetime import datetime

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


def main():
    module = AnsibleModule(
        argument_spec=dict({})
    )

    end_time = datetime.utcnow().strftime("%d-%b-%Y %H:%M:%S")


    data = dict(
        output="end-time stored called successfully",
    )
    try:
        if os.path.exists(filename):  # open file to append
            with open(filename, 'a') as outfile:
                outfile.seek(-1, os.SEEK_END)
                outfile.truncate()
                outfile.write(',')
                outfile.write('\n')
                outfile.write("\"end-time\"" + ": " + '"{}"'.format(end_time))
                outfile.write("}")
                outfile.close()

        else:  # create a new file
            with open(filename, 'w') as outfile:
                outfile.write("{")
                outfile.write('\n')
                outfile.write("\"end-time\"" + ": " + '"{}"'.format(end_time))
                outfile.write("}")
                outfile.close()
    except Exception as e:
        module.fail_json(msg='Error in record-start-time')

    module.exit_json(changed=True, success=data, msg=end_time)


if __name__ == '__main__':
    main()
