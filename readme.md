## NeCTAR/OpenStack Cloud Provision with Boto
This tute demo how to use the AWS cloud provision tool [boto](https://github.com/boto/boto) (_A Python interface to Amazon Web Services_) with [NeCTAR Cloud](https://nectar.org.au/) - _Australia National eResearch Collaboration Tools and Resources_. Though boto is [AWS oriented](https://aws.amazon.com/sdk-for-python/), it can also be used in an [OpenStack](https://www.openstack.org/user-stories/nectar/) based cloud infrastructure.


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

### Running Scripts

```commandline
python connection.py
python images.py
python vm.py
```

---
For more scripting and API choices:
 http://boto.cloudhackers.com/en/latest/