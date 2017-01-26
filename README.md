
Ansible Async Wrapper
=====================================

##### allows to play whole playbook independently on each host
##### without waiting for a last finisher on each task
=====================================

When executing same task on a lot of hosts with execution time that depends on each specific host in cluster you may consider to run these playbooks fully independently on each host, so you not obligated to wait last finishers on each task.
#### Note
* Working thru the '--limit' option when inventory file submitted makes all your group variables in place (if any)
* For now, not checking for 'hosts: group' in playbook, reading all hosts from inventory file

#### Usage
####
```sh
$ python async.py -i /path/to/hosts_file playbook.yml
or
$ python async.py -i "host1.domain.name,host2.domain.name,..." playbook.yml
```
#### Options
####
```sh
max_workers = 10    ------->      max threads
log = True          ------->      log mode
logdir = '.log'     ------->      log path
```
