from configparser import ConfigParser


def main():
    conf = ConfigParser()
    conf.read('config.ini')

    conf['credentials']['aws_access_key_id'] = 'INSERT_YOUR_ACCESS_KEY_FROM-ec2rc.sh'
    conf['credentials']['aws_secret_access_key'] = 'INSERT_YOUR_SECRET_KEY_FROM-ec2rc.sh'
    conf['default']['key_name'] = 'INSERT_YOUR_KEY_PAIR_NAME'
    conf['local']['key_file_path'] = '/home/username/path/to/key/location'
    conf['local']['key_file'] = 'cloud_key_pair.key'

    with open('config.ini.sample', 'w') as sample:
        conf.write(sample)


if __name__ == '__main__':
    main()
