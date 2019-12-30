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


def main():
    module = AnsibleModule(
        argument_spec=dict({})
    )

    hostname = socket.gethostname()

    data = dict(
        output="run-client stored called successfully",
    )
    try:
        if os.path.exists(filename):  # open file to append
            with open(filename, 'a') as outfile:
                outfile.seek(-1, os.SEEK_END)
                outfile.truncate()
                outfile.write(',')
                outfile.write('\n')
                outfile.write("\"run-client\"" + ": " + '"{}"'.format(hostname))
                outfile.write("}")
                outfile.close()

        else:  # create a new file
            with open(filename, 'w') as outfile:
                outfile.write("{")
                outfile.write('\n')
                outfile.write("\"run-client\"" + ": " + '"{}"'.format(hostname))
                outfile.write("}")
                outfile.close()
    except Exception as e:
        module.fail_json(msg='Error in get-run-client')

    module.exit_json(changed=True, success=data, msg=hostname)


if __name__ == '__main__':
    main()
