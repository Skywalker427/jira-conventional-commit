#!/usr/bin/python3

import sys
import os
import subprocess
import re

auto_confirm = False
JIRA_BRANCH_PATTERN = r'^([\w\d]+-\d+)-[\w\d-]+$'

def get_branch_name():
    cmd = 'git branch --show-current'
    branch_name = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    return branch_name

# Branch name should be in format: TEAM-1234-feature-name-of-branch
def is_valid_jira_branch_name(branch_name):
    return bool(re.match(JIRA_BRANCH_PATTERN, branch_name))

# Return TEAM-1234 from TEAM-1234-feature-name-of-branch
def get_ticket_from_branch(branch_name):
    return re.match(JIRA_BRANCH_PATTERN, branch_name).group(1)

def get_conventional_commit_type(commit_arg):
    conventional_commits = {
       'feat': ['f', 'feat', 'feature', 'ft'],
        'fix': ['fx', 'fix'],
        'docs': ['d', 'docs'],
        'style': ['s', 'style', 'st'],
        'refactor': ['r', 'refactor', 'ref'],
        'test': ['t', 'test'],
        'chore': ['c', 'chore'],
        'perf': ['p', 'perf'],
        'ci': ['ci'],
        'build': ['b', 'build', 'bld', 'bl', 'bd'],
        'revert': ['rev', 'revert'],
        'wip': ['wip'],
        'release': ['rl', 'release'],
        'hotfix': ['hf', 'hfx', 'hotfix'],
        'merge': ['m', 'merge'],
        'squash': ['sq', 'squash'],
    }
    for commit_type, aliases in conventional_commits.items():
        if commit_arg in aliases:
            return commit_type
    return 'chore'

def get_cmd_arguments():
    return sys.argv[1:]

def get_commit_type_and_message():
    args = get_cmd_arguments()
    if len(args) == 1:
        return get_conventional_commit_type('chore'), args[0]
    elif len(args) == 2:
        args[0] = args[0].replace('-', '')
        return get_conventional_commit_type(args[0]), args[1]
    elif len(args) == 3: 
        global auto_confirm 
        auto_confirm = args[2].replace('-', '') in ['y', 'yes']
        args[0] = args[0].replace('-', '')
        return get_conventional_commit_type(args[0]), args[1]
    else:
        return None, None

def generate_conventional_commit_message(commit_type, commit_message):
    if not commit_type or not commit_message:
        print('>>> Invalid number of arguments. Please provide a commit message or commit type and message. <<<')
        sys.exit(1)
    ticket = get_ticket_from_branch(get_branch_name())
    return f'{commit_type}: [{ticket}] {commit_message}'

def get_staged_files():
    cmd = 'git diff --name-only --cached'
    staged = subprocess.check_output(cmd, shell=True).decode('utf-8').split('\n')
    return list(filter(lambda x: x != '', staged))

def commit(commit_message):
    cmd = f'git commit -m "{commit_message}"'
    os.system(cmd)

# pretty print commit type and message as tabled output
def print_type_and_message(commit_type, commit_message):
    # get the length of the longest commit type
    longest_commit_type = 10
    commit_message_length = commit_message.__len__() + 2
    if commit_type.__len__() > longest_commit_type:
        longest_commit_type = commit_type.__len__()
    #print 'type' and 'message' centered as headers
    print(f'┌{"─" * longest_commit_type}┬{"─" * commit_message_length}┐')
    print(f'│{"type":^{longest_commit_type}}│{"message":^{commit_message_length}}│')
    # print the commit type and message as a table
    print(f'┌{"─" * longest_commit_type}┬{"─" * commit_message_length}┐')
    print(f'│{commit_type:^{longest_commit_type}}│{commit_message:^{commit_message_length}}│')
    print(f'└{"─" * longest_commit_type}┴{"─" * commit_message_length}┘')
    print('\n')



def confirm_commit(commit_type, commit_message):
    staged_files = get_staged_files()
    if len(staged_files) == 0:
        print('No staged files. Nothing to commit.\n\n')
        sys.exit(0)
    print_type_and_message(commit_type, commit_message)
    print(f'Staged files: {staged_files}\n\n')
    confirmation = input('Are you sure you want to commit? (y/n): ') if not auto_confirm else 'y'
    return confirmation


if __name__ == '__main__':
    branch_name = ''
    try:
        branch_name = get_branch_name()
    except subprocess.CalledProcessError:
        print('Not a git repository. Please run this command in a git repository.\n\n')
        sys.exit(1)
    if not is_valid_jira_branch_name(branch_name):
        print(f'Branch name <{branch_name.strip()}> is not a valid jira branch!')
        print('Please checkout a valid jira branch and try again.\n\n')
        sys.exit(1)
    else:
        commit_type, commit_message = get_commit_type_and_message()
        commit_message = generate_conventional_commit_message(commit_type, commit_message)
        confirmation = confirm_commit(commit_type,commit_message)
        if confirmation.lower() in ['y', 'yes']:
          print(f'Committing to {branch_name}\n')
          commit(commit_message)
        else:
          print('Commit aborted.\n\n')
        sys.exit(0)
