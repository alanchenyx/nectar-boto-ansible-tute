import time

import config
import connection

conn = connection.establish()

my_instances = set()


def create_server():
    user_data_script = """#!/bin/bash
    echo "Hello World" >> /tmp/data.txt"""

    new_reservation = conn.run_instances(
        config.default_image_id(),
        key_name=config.default_key_name(),
        instance_type=config.default_instance_type(),
        security_groups=config.default_security_groups(),
        user_data=user_data_script)

    new_instance = new_reservation.instances[0]

    # NOTE: This does not reflect what seem as 'Instance Name' on Nectar dashboard.
    # conn.create_tags([new_instance.id], {'Name': config.default_instance_name()})

    while new_instance.state == u'pending':
        print('Creation status: {}'.format(new_instance.state))
        time.sleep(10)
        new_instance.update()

    # NOTE: The ip_address return None on Nectar but private_ip_address return the public IP.
    print('Done. Instance {} with IP {} in zone {} is {}.'
          .format(new_instance.id, new_instance.private_ip_address, new_instance.placement, new_instance.state))


def show_reservations_and_instances():
    reservations = conn.get_all_reservations()
    if len(reservations) < 1:
        print('You have no instances provisioned.')
    else:
        for res in reservations:
            print('Reservation {} has {} instances.'.format(res.id, len(res.instances)))
            for inst in res.instances:
                # print(inst.__dict__)  # dump all
                print('\t{} {} {} {}'.format(inst.id, inst.private_ip_address, inst.placement, inst.state))
                my_instances.add(inst.id)


def show_instances():
    # Alternatively, it can use get_only_instances() instead of going through get_all_reservations()
    # instances = conn.get_only_instances()
    pass


def main():
    show_reservations_and_instances()

    print('=' * 100)
    uin = input('Create new instance (y or n): ')
    if uin == 'y':
        create_server()
    elif uin == 'n':
        print('Alright!')
    else:
        print('Excuse me?')

    if len(my_instances) < 1:
        exit()

    print('=' * 100)
    uin = input('Start all instances (y or n): ')
    if uin == 'y':
        conn.start_instances(list(my_instances))
        time.sleep(10)
        show_reservations_and_instances()
    elif uin == 'n':
        print('Fine!')
    else:
        print('Pardon?')

    print('=' * 100)
    uin = input('Stop all instances (y or n): ')
    if uin == 'y':
        conn.stop_instances(list(my_instances))
        time.sleep(10)
        show_reservations_and_instances()
    elif uin == 'n':
        print('Ok!')
    else:
        print('Why?')

    print('=' * 100)
    uin = input('[WARNING] Terminate all instances (y or n): ')
    if uin == 'y':
        conn.terminate_instances(list(my_instances))
        time.sleep(10)
        show_reservations_and_instances()
    elif uin == 'n':
        print('Fair enough!')
    else:
        print('What?')


if __name__ == '__main__':
    main()
