# cSHAKE

1. cSHAKEPython: rdtsc is from James Brown, which is used to get CPU cycle count. cSHAKE.py is a pure python implementation for cSHAKE hash function. I modify the official python implementation of Keccak to make a implementation of cSHAKE.

2. cSHAKElib: rdtsc is from James Brown, which is used to get CPU cycle count. cSHAKE128.py and cSHAKE256.py are from Legrandin, which are both SHAKE hash function. I modify some parameters to support cSAHKE hash function.

Instruction

This instruction is based on running on Ubuntu. If the implementation has to be run on other operation systems, such as macOS or CentOS, commands should be slightly modified. In addition, it only pass the test on Python 2.7.

First of all, we need to update and upgrade advanced packaging tools, then install git and pip.

$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install git
$ sudo apt-get install python-pip

Then we need to install python library (cSHAKElib requiring).

$ sudo pip install pycryptodome

After that we need to get clone from github.
$ git clone https://github.com/Hemoth/cSHAKE.git

Finally, we can use this command to run the implementation.

$ python cSHAKE/cSHAKElib/test_cSHAKE.py
$ python cSHAKE/cSHAKEPython/test_cSHAKE.py

API examples

output = cSHAKE128(inputString, outputLength, customParameter)
output = cSHAKE256(inputString, outputLength, customParameter)
