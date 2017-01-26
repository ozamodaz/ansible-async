'''
Note!

* Working thru the '--limit' option when inventory file submitted
  makes all your group variables in place (if any)

* For now, not checking for 'hosts: group' in playbook,
  reading all hosts from inventory file
'''
import argparse
from concurrent.futures import ThreadPoolExecutor
import os
import re

max_workers = 10
log = True
logdir = '.log'
if not os.path.exists(logdir):
    os.makedirs(logdir)


parser = argparse.ArgumentParser(description='Ansible Async Wrapper')
parser.add_argument('playbook', metavar='playbook.yml', type=str, nargs=1,
                           help='path to Ansible playbook')
parser.add_argument('-i', dest='inventory', type=str, nargs=1, required=True,
             help='specify inventory host path or comma separated host list')

def inventory_file(inventory):
    hosts = []
    ip_addr = re.compile('^(?:[0-9]{1,3}\.){3}[0-9]{1,3}')
    host_name = re.compile('^(?:[a-z1-9-_]+\.)+[a-z]+')
    blank = re.compile('^\s+')
    grp_name = re.compile('^\[\w+\]')
    comment = re.compile('^#')
    for line in open(inventory, 'r').read().splitlines():
        if grp_name.search(line) or comment.search(line) or blank.search(line):
            pass
        elif ip_addr.search(line):
            hosts.append(ip_addr.search(line).group())
        elif host_name.search(line):
            hosts.append(host_name.search(line).group())
    return hosts


args = parser.parse_args()
inventory = args.inventory[0]
playbook = args.playbook[0]

if ',' in inventory:
    hosts = [host.strip() for host in inventory.split(',')]
    hosts_file = False
else:
    hosts = inventory_file(inventory)
    hosts_file = True

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    for host in hosts:
        limit = '--limit %s' % host if hosts_file else ''
        inventory = ','.join(hosts) if not hosts_file else inventory
        log = '> %s/%s' % (logdir, host) if log else ''
        call = 'ansible-playbook -i "%s" %s %s %s' % \
                   (inventory, limit, playbook, log)
        worker = executor.submit(os.system, call)
