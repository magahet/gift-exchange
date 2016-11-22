Gift Exchange
=============

Generates a random gift exchange assignment while avoiding predefined conflicts.

The only implemented conflict check is that no one should be assigned a member of their own family. More checks can be added.

Can email each person with their assignment.


## Usage

    $ ./random-pick.py -h
    usage: random-pick.py [-h] [-d] [-e] people

    positional arguments:
      people        yaml file with list of individuals

      optional arguments:
        -h, --help    show this help message and exit
        -d, --debug   Send emails to sender address for testing
        -e, --emails  Send emails


    $ ./random-pick.py -d example-list.yaml 
    Creating random list...
    Done
    Bob, Dan, Alice, Carl, Fred, Eve
