## NeCTAR Cloud Provision with Boto and Ansible
This tute demo how to use the cloud provision tools [boto](https://github.com/boto/boto) (_A Python interface to Amazon Web Services_) and [Ansible](https://github.com/ansible/ansible) with [NeCTAR Cloud](https://nectar.org.au/) - _Australia National eResearch Collaboration Tools and Resources_. Though boto is [AWS oriented](https://aws.amazon.com/sdk-for-python/), it can also be used in an [OpenStack](https://www.openstack.org/user-stories/nectar/) based cloud infrastructure.


### Notes for Windows

1. Using [Intel® Distribution for Python](https://software.intel.com/en-us/intel-distribution-for-python) which have [Free for Student](https://software.intel.com/en-us/qualify-for-free-software/student) copy. After installation, add `C:\IntelPython35` to `PATH` environment variable so that it can access from `cmd.exe`.

```
> python -V
Python 3.5.2 :: Intel Corporation
> pip install boto
> python -c "import boto"
> python
>>> import boto
>>> print (boto.__version__)
2.46.1
>>> exit()
```

2. The standard [Python](http://www.python.org/) distribution also work. Just that Intel distribution is used for convenient.


### Notes for `config.ini` and Credentials

1. Login to [Nectar Cloud](https://dashboard.rc.nectar.org.au/)

2. Select your project then go to:
`Compute > Access & Security > API Access tab > Download EC2 Credentials` to download and extract the zip contents.

3. Open `ec2rc.sh` in _Notepad++_

4. Copy [`config.ini.sample`](config.ini.sample) to `config.ini`

5. Copy values `aws_access_key_id` and `aws_secret_access_key` from `ec2rc.sh` to `config.ini`.

6. Tailor any other config values in `config.ini`.

### Running Boto Scripts

```commandline
python connection.py
python images.py
python vm.py
```

### Notes for Ansible on Windows
Since Ansible [key dependency is OpenSSH](https://en.wikipedia.org/wiki/Ansible_(software)#Design_goals), it bakes nicely with any UNIX/Linux flavours. On Windows, you will need this *Nix OS base capability. The options are:
  * [Windows Subsystem for Linux (WSL)](https://msdn.microsoft.com/en-au/commandline/wsl/about)
  * Cygwin
  * VirtualBox or HyperV

I've tried Cygwin but no success. The idea for VirtualBox or HyperV is to setup Linux VM and use Ansible. However it requires running the development iteration on the VM. I go with WSL and it works but it requires Windows 10.
   
* Setup WSL as guided in [this article](https://msdn.microsoft.com/en-au/commandline/wsl/install_guide) and launch _Bash on Ubuntu on Windows_.
 
* We need Python3.
```commandline
which python3
python3 -V

sudo apt install python3-pip
which pip3
pip3 -V

pip3 install ansible --user
```

* You might get this error.
```
...
"fatal error: ffi.h: No such file or directory"
...
```

* Install the required library.
```commandline
sudo apt install libffi-dev
```

* You might get this error.
```
...
"fatal error: Python.h: No such file or directory"
...
```

* Install the required library.
```commandline
sudo apt install python3-dev
```

* Now install Ansible to user directory.
```commandline
pip3 install ansible --user
```

* The switch `--user` installs Ansible binaries into the user home `.local/bin` directory.
```commandline
username@host:~$ cd
username@host:~$ ls -l .local/bin/
total 56
-rwxrwxrwx 1 user user 4792 Apr 10 02:53 ansible
-rwxrwxrwx 1 user user 4792 Apr 10 02:53 ansible-console
-rwxrwxrwx 1 user user 4792 Apr 10 02:53 ansible-doc
-rwxrwxrwx 1 user user 4792 Apr 10 02:53 ansible-galaxy
-rwxrwxrwx 1 user user 4792 Apr 10 02:53 ansible-playbook
-rwxrwxrwx 1 user user 4792 Apr 10 02:53 ansible-pull
-rwxrwxrwx 1 user user 4792 Apr 10 02:53 ansible-vault
```

* Add to the `PATH`.
```
echo 'PATH=$HOME/.local/bin:$PATH' >> .bashrc
source .bashrc
which ansible
which ansible-playbook

ansible --version
```

* You might get this error.
```
"ImportError: No module named 'markupsafe'"
```

* Install the required library.
```commandline
sudo pip3 install markupsafe

ansible --version
```

* We also need boto in this environment.
```commandline
sudo pip3 install boto
```

### Running Boto + Ansible Scripts

Finally, we can run `automaton.py` which is a combination of Boto and Ansible. It will provision the Nectar cloud resource using Boto and then configure with it with Ansible. Note that it has to invoke from _Bash on Ubuntu on Windows_.

```commandline
python3 automaton.py
```

Sample Output:
```
$ python3 automaton.py

You have no instance. Create one? (y or n): y
Creation status: pending
Creation status: pending
Done. Instance i-9f7168f7 with IP 123.45.678.9xx in zone NCI is running.

0:      i-9f7168f7      123.45.678.9xx  running NCI

Pick an instance number: 0

PLAY [webservers] **************************************************************

TASK [setup] *******************************************************************
The authenticity of host '123.45.678.9xx (123.45.678.9xx)' can't be established.
ECDSA key fingerprint is xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx.
Are you sure you want to continue connecting (yes/no)? yes
ok: [123.45.678.9xx]

TASK [install apache2] *********************************************************
changed: [123.45.678.9xx]

PLAY RECAP *********************************************************************
123.45.678.9xx             : ok=2    changed=1    unreachable=0    failed=0

Web server is accessible at http://123.45.678.9xx

$ python3 vm.py
Reservation r-4iqxsk3i has 1 instances.
        i-9f7168f7 123.45.678.9xx NCI running
====================================================================================================
Create new instance (y or n): n
Alright!
====================================================================================================
Start all instances (y or n): n
Fine!
====================================================================================================
Stop all instances (y or n): n
Ok!
====================================================================================================
[WARNING] Terminate all instances (y or n): y
You have no instances provisioned.
```


---
For more scripting and API choices:
 * http://boto.cloudhackers.com/en/latest/
 * http://docs.ansible.com/