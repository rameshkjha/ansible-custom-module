# ansible-custom-module
Custom ansible module which can be called from any playbook - and it will create a log/json file on client machine with all the details. 

{
"client-name" : "jha-mac",
"run-on" : ["127.0.0.1"],
"start-time" : "12-Dec-2019 HH:MM:SS",
"end-time" : "12-Dec-2019 HH:MM:SS"
}

Custom modules have dependency on AnsibleModule from ansible.module_utils.basic. All these cusom module files (python files) must be stored under ./ansible/lib directory.
If you don't have cloned ansible repository, then run clone the repository first before you use these custom modules.
Command to clone ansible modules.
cd <to directory where you want to store ansible artifacts>
git clone https://github.com/ansible/ansible.git

You must set export ANSIBLE_LIBRARY=/Users//tools/ansible/lib/ <absolute path of your ./lib directory where custom modules are stored>

You must call generate_playbook_log at least in your playbook as first task, rest depending upon your need either you can use it or leave it.

 - name: fetch local hostname 
   hosts: localhost
   gather_facts: no
   tasks:
     - name: generate playbook log
       generate_playbook_log:
