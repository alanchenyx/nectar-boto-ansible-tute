import configparser
import os
import shlex
import subprocess
import sys
import time

import config
import vm

conn = vm.conn
instances = conn.get_only_instances()
parser = configparser.ConfigParser(allow_no_value=True, delimiters=' ')


def main():
    print('')
    if len(instances) < 1:
        uin = input('You have no instance. Create one? (y or n): ')
        if uin == 'y':
            vm.create_server()
            time.sleep(5)
            instances.extend(conn.get_only_instances())
            print('')
        else:
            print('Abort')
            exit()

    for idx, inst in enumerate(instances):
        print('{}:\t{}\t{}\t{}\t{}'.format(idx, inst.id, inst.private_ip_address, inst.state, inst.placement))

    idx = 0
    try:
        print('')
        idx = int(input('Pick an instance number: '))

        if idx not in range(0, len(instances)):
            print('Not a good choice! Abort...')
            exit()

    except ValueError:
        print('Naughty? Abort...')
        exit()

    instance = instances[idx]

    if instance.state != 'running':
        uin = input('Instance {} is {}. Do you want to start it? (y or n): '.format(instance.id, instance.state))
        if uin == 'y':
            print('Starting instance {}...'.format(instance.id))
            conn.start_instances(instance.id)
            while instance.state == u'stopped':
                print('.', end='')
                sys.stdout.flush()
                time.sleep(1)
                instance.update()
            print('\nInstance {} is now {}.'.format(instance.id, instance.state))
        else:
            print('Abort')
            exit()

    # NOTE: Ansible is idempotent

    parser['webservers'] = {instance.private_ip_address: ''}

    with open('hosts.ini', 'w') as host_file:
        parser.write(host_file)

    key_file_path = config.parser['local']['key_file_path']
    key_file = config.parser['local']['key_file']

    command_line = 'ansible-playbook'
    command_line += ' -i hosts.ini'
    command_line += ' -u ubuntu'
    command_line += ' -b --become-method=sudo'
    command_line += ' --key-file=' + os.path.join(key_file_path, key_file)
    command_line += ' automaton.yaml'
    # print(command_line)

    args = shlex.split(command_line)
    # print(args)

    # TODO: known issue - the first invocation of Ansible has SSH error. 2nd time is ok.
    '''
    fatal: [xxx.xx.xxx.xxx]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: ssh: 
    connect to host xxx.xx.xxx.xxx port 22: Connection refused\r\n", "unreachable": true}
    '''
    process = subprocess.Popen(args, shell=False)
    process.communicate()

    print('Web server is accessible at http://{}'.format(instance.private_ip_address))
    print('')


if __name__ == '__main__':
    main()
