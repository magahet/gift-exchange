#!/usr/bin/env python
'''This app builds a random gift exchange list following a set of rules'''


import yaml
import random
import argparse
import smtplib
import getpass


def main():
    '''Get params and run random list creator.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('people', help='yaml file with list of individuals')
    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='Send emails to sender address for testing')
    parser.add_argument('-e', '--emails', action='store_true', default=False,
                        help='Send emails')
    args = parser.parse_args()
    random_list = create_random_list(args.people)
    if args.debug:
        print_list(random_list)
    if args.emails:
        send_emails(random_list, debug=args.debug)


def print_list(random_list):
    '''Print results.'''
    print ', '.join([p.get('name') for p in random_list])


def create_random_list(people_file):
    '''Shuffle list and test against conflict functions.'''
    print 'Creating random list...'
    people = load_yaml(people_file)
    random.shuffle(people)
    while has_conflicts(people):
        random.shuffle(people)
    print 'Done'
    return people


def load_yaml(path):
    '''Load a yaml file.'''
    with open(path, 'r') as file_:
        return yaml.load(file_)


def has_conflicts(people):
    '''Check for conflicts.'''
    check_funcs = [same_family]
    for func in check_funcs:
        if func(people):
            return True
    return False


def same_family(people):
    '''Same family.'''
    for person, assigned in iter_people(people):
        if assigned.get('name') in person.get('family', []):
            return True
    return False


def send_emails(people, debug=False):
    '''Send emails to each person with their assigned buddy.'''
    print 'Sending emails...'
    gmail_user = raw_input('Gmail user: ').strip()
    gmail_password = getpass.getpass()
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
    except Exception as error:
        print 'Could not connect to email server.'
        print error
        return
    for person, assigned in iter_people(people):
        to_address = gmail_user if debug else person.get('email')
        email_text = ''.join([
            'From: {}\n'.format(gmail_user),
            'To: {}\n'.format(to_address),
            'Subject: Gift exchange buddy\n\n',
            '{},\n\n'.format(person.get('name')),
            'Your gift exchange buddy is {}.\n'.format(assigned.get('name')),
        ])
        try:
            server.sendmail(gmail_user, to_address, email_text)
        except:
            print 'Error sending email to: {}'.format(person.get('name'))
    server.close()
    print 'Done'


def iter_people(people):
    '''Iterate through people returning a person and their assigned person.'''
    for index in xrange(len(people)):
        yield people[index], people[(index + 1) % len(people)]


if __name__ == '__main__':
    main()
