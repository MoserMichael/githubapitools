#!/usr/bin/env python3

import os
import shlex
import subprocess
import sys
import re
import time
import ctypes
import argparse
from pathlib import Path
from platform import system
from github import Github

# *** adapted from https://raw.githubusercontent.com/nekumelon/simpleSound/main/simpleSound.py ***


def windows_command(command):
    ctypes.windll.winmm.mciSendStringW(command, ctypes.create_unicode_buffer(600), 559, 0)

def play(file_name):
    os_name = system()

    if os_name == "Windows":
        windows_command("open " + file_name)
        windows_command("play " + file_name + " wait")
        windows_command("close " + file_name)
    else:
        cmd = ''
        if os_name == "Darwin":
            cmd = "exec afplay \"" + file_name + "\""
        elif os_name == "Linux":
            cmd = "exec aplay --quiet " + file_name
        else:
            print("can't play sound on ",os_name)
            return

        with subprocess.Popen(cmd, universal_newlines = True, shell = True, stdout = -1, stderr = -1) as proc:
            proc.communicate()

def beep(success):
    if success:
        data_file = Path(__file__).with_name('Blow.aiff')
    else:
        data_file = Path(__file__).with_name('Basso.aiff')
    play(str(data_file))

# *** eof copied ***


class RunCommand:
    trace_on = False
    exit_on_error = True

#    @staticmethod
#    def trace(on_off):
#        RunCommand.trace_on = on_off
#
#    @staticmethod
#    def exit_on_error(on_off):
#        RunCommand.exit_on_error = on_off
#
    def __init__(self, command_line = None):
        self.command_line = command_line
        self.exit_code = 0
        if command_line is not None:
            self.run(command_line)

    def run(self, command_line):
        try:
            if RunCommand.trace_on:
                print('>', command_line)

            with subprocess.Popen(shlex.split(command_line), \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:

                self.command_line = command_line

                (output, error_out) = process.communicate()

                self.exit_code = process.wait()

                self.output = output.decode("utf-8")
                self.error_out = error_out.decode("utf-8")


                self.exit_code = process.wait()

                if RunCommand.trace_on:
                    msg = ">exit_code: " + str(self.exit_code)
                    if self.output != "":
                        msg += "\n  stdout: " + self.output
                    if self.error_out != "":
                        msg += "\n  stderr: " + self.error_out
                    print(msg)

                if RunCommand.exit_on_error and self.exit_code != 0:
                    print(self.make_error_message())
                    sys.exit(1)

                return self.exit_code
        except FileNotFoundError:
            self.output = ""
            self.error_out = "file not found"
            self.exit_code = 1
            return self.exit_code

    def result(self):
        return self.exit_code, self.output

    def make_error_message(self):
        return_value = ""
        if self.command_line != "":
            return_value += f" command line: {self.command_line}."
        if self.exit_code != 0:
            return_value += f" exit status: {self.exit_code}. "
        if self.error_out != "":
            return_value += " " + self.error_out
        return return_value

def init():
    cmd = RunCommand()

    if cmd.run("git rev-parse --show-toplevel" ) != 0:
        print("Error: current directory not part of git tree")
        sys.exit(1)

    if cmd.run("git show -s --format=%H") != 0:
        print("Error: can't get top commit", cmd.make_error_message())
        sys.exit(1)
    top_commit = cmd.output.rstrip('\n')

    if  cmd.run("git branch -r --contains " + top_commit) != 0:
        print("Error: top commit ", top_commit, "has not been pushed yet", cmd.make_error_message())
        sys.exit(1)

    if cmd.run("git rev-parse --abbrev-ref HEAD") != 0:
        print("Error: can't get current branch name", cmd.make_error_message())
        sys.exit(1)
    local_branch_name = cmd.output.rstrip('\n')

    if cmd.run('/bin/bash -c \'git status -b --porcelain=v2 | grep -m 1 "^# branch.upstream " | cut -d " " -f 3-\'') != 0:
        print("Error: can't get name of remote branch", cmd.make_error_message())
        sys.exit(1)
    remote_branch_name = cmd.output.rstrip('\n')

    if cmd.run("git show -s --format='%s %h'") != 0:
        print("Error: can't get last commit comment", cmd.make_error_message())
        sys.exit(1)
    last_commit_sha_and_comment = cmd.output.rstrip('\n')

    if cmd.run("git show -s --format='%b'") != 0:
        print("Error: can't get body of last commit", cmd.make_error_message())
        sys.exit(1)
    last_commit_body = cmd.output

    if cmd.run("git config --get remote.origin.url") != 0:
        print("Error: can't get remote origin url", cmd.make_error_message())
        sys.exit(1)

    remote_origin = cmd.output
    pos_1 = remote_origin.rfind('/')
    pos_2 = remote_origin.rfind('.')
    if pos_1 == -1 and pos_2 == -1:
        print("Error: can't get repository namefrom remote url: ", remote_origin)

    repo_name = remote_origin[pos_1+1:pos_2]
    if repo_name == "":
        print("Error: can't get repository namefrom remote url: ", remote_origin, " ", cmd.make_error_message())
        sys.exit(1)

    print("top_commit:", top_commit, \
            "repo_name:", repo_name, \
            "local_branch_name:", local_branch_name, \
            "remote_branch_name: ", remote_branch_name, \
            "last-commit-comment:", last_commit_sha_and_comment, \
            "last-commit-body: ", last_commit_body)
    return top_commit, repo_name, local_branch_name, remote_branch_name, last_commit_sha_and_comment, last_commit_body


def wait_for_commit_to_build(repo, commit):
    commit = repo.get_commit(commit)
    print(commit)

    print("Waiting for the build to complete...")
    if RunCommand.trace_on:
        print("Commit: ", commit)
        print(repo.full_name)

    while True:
        if not RunCommand.trace_on:
            print(".", end="", flush=True)
        else:
            print("\nchecking statuses...")

        for status in commit.get_statuses():
            if RunCommand.trace_on:
                print( "created_at", status.created_at ,"creator:", status.creator,  " id:", status.id, "state:", status.state, "context:", status.context, "target_url:", status.target_url,  "url:", status.url, "description:", status.description )

            if status.context == "build":
                if status.state == "success":
                    return  True, status.target_url
                if status.state == "failure":
                    return  False, status.target_url

        time.sleep(5)

def create_branch_and_pr(repo, local_branch_name, last_commit_sha_and_comment, last_commit_body):

    local_br_name = last_commit_sha_and_comment
    local_br_name = re.sub(r"[^a-zA-Z0-9\ ]+",'', local_br_name)
    local_br_name = re.sub(r"\s+", '-', local_br_name)

    cmd = RunCommand()

    print("local_br_name; ", local_br_name)

    #if cmd.run("git checkout -b " + local_br_name) != 0:
    if cmd.run("git branch -m " + local_br_name) != 0:
        print("Error: can't rename branch to  branch_name", cmd.make_error_message())
        sys.exit(1)

    if cmd.run("git push --set-upstream origin " + local_br_name + ":feature/" + local_br_name) != 0:
        print("Error: can't push to feature/" + local_br_name, " ", cmd.make_error_message())
        sys.exit(1)

    base_name = "feature/" + local_br_name
    #head_name = "remotes/origin/" + local_branch_name
    head_name = local_branch_name
    print("create_pull_request base:", head_name, "head:", base_name)

    # doc for create_repo:  https://docs.github.com/en/rest/reference/pulls#create-a-pull-request

    pull_request = repo.create_pull(
            title=last_commit_sha_and_comment,
            body=last_commit_body,
            base=head_name,
            head=base_name,
            maintainer_can_modify=True
            )

    print("pull request created: ", pull_request)

def parse_cmd_line():

    usage = '''
This program does the following steps; it assumes that the current directory is in a git tree.

for the --new-pr option:
    1. Creates a feature branch for the current branch, and pushes the feature branch.
    2. Opens a pull request, it is assumed that a continuous integration build is then triggered.
    3. The program then waits that the continuous integration build for that pull request has completed.
    4. At the end of the build, a sound is played, and the url with the build log is written to standard output.

for the --update-pr option:
    1. Push the current state of local branch to the feature banch
    2. The program waits that the continuous integration build for the top commit has completed.
    3. At the end of the build, a sound is played, and the url with the build log is written to standard output.

for the --wait option:
    2. The program waits that the continuous integration build for the top commit has completed.
    3. At the end of the build, a sound is played, and the url with the build log is written to standard output.

Note that you need to set the organization (-o option) in the case of a private repository.

This program allows you to do some sword fighting, while the continuous integration build is going on ;-(

This program assumes that the environment GITHUB_TOKEN is exported, and that it has the token of the current user.
This program assumes the github api to be installed - pip install python-github-api

'''
    parse = argparse.ArgumentParser(description=usage, \
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    group = parse.add_argument_group("Push or update a pull request and wait for the continuous integration build to complete")

    group.add_argument('--new-pr', '-n',  default=False, \
            action='store_true', dest='new_pr', help='create new pull request')

    group.add_argument('--update-pr', '-u',  default=False, \
            action='store_true', dest='update_pr', help='update and push to existing pull request')

    group.add_argument('--wait', '-w',  default=False, \
            action='store_true', dest='wait', help='wait for ongoing build of top commit to complete')

    group.add_argument('--org', '-o',  default='', \
            type=str, dest='org', help='specify organization used to lookup the repository')

    group.add_argument('--showlog', '-s',  default=False, \
            action='store_true', dest='showlog', help='show the build log in a browser window')

    group.add_argument('--verbose', '-v',  default=False, \
            action='store_true', dest='verbose', help='trace all commands, verbose output')


    return parse.parse_args(), parse

def push_state_to_branch(remote_branch_name):
    if not remote_branch_name.startswith("origin/feature/"):
        print("Error. Remote origin does not start with 'origin/feature', curent remote branch name is:", remote_branch_name)
        sys.exit(1)

    cmd = RunCommand()
    if cmd.run("git push origin HEAD:" + remote_branch_name[7:]) != 0:
        print("Error: can't push  local changes. ", cmd.make_error_message())
        sys.exit(1)

def show_build_log(url):
    # show it in a web browser.
    # can't get the data through websockets via api call: the page may need non trivial authentication, for private repos.
    import webbrowser
    webbrowser.open(url)

##   keep getting 200 ok instead of 101 upgrade for private repos...
#    ws_url = url.replace("https://", "wss://")
#    print("ws_url:", ws_url)
#
#    import websocket
#    import ssl
#
#    websocket.enableTrace(True)
#    ws = websocket.create_connection(ws_url,
#            sslopt={
#                "cert_reqs": ssl.CERT_NONE,
#                "check_hostname": False
#                },
#            header = [ "Sec-Fetch-Dest: websocket",
#                       "Sec-Fetch-Mode: websocket",
#                       "Sec-Fetch-Site: same-origin" ,
#                       "Sec-WebSocket-Key: 7Ygmm93Vo8zp+fhpcmUEMg==",
#                       "Sec-WebSocket-Extensions: permessage-deflate",
#                       "Connection: keep-alive, Upgrade",
#                       "Cache-Control: no-cache",
#                       "Pragma: no-cache",
#                       "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
#                       "Accept: */*",
#                       "Accept-Language: en-US,en;q=0.5",
#                       "Accept-Encoding: gzip, deflate, br" ])
#
#
#    ws.send("Hello, World")
#    result = ws.recv()
#    print("Received '%s' type:  %s" % (result, str(type(result))) )
#    ws.close()
#
#    import ssl
#
#    # non verifying ssl context (https://stackoverflow.com/questions/30461969/disable-default-certificate-verification-in-python-2-7-9)
#    ssl_ctx = ssl.create_default_context()
#    ssl_ctx.check_hostname = False
#    ssl_ctx.verify_mode = ssl.CERT_NONE
#
#    import asyncio
#    from websockets import connect
#
#    async def hello(uri):
#        async with connect(uri,ssl=ssl_ctx) as websocket:
#            await websocket.send("Hello world!")
#            resp = await websocket.recv()
#            print(resp)
#
#    asyncio.run(hello(ws_url))


def main():
    cmd_args, _ = parse_cmd_line()

    if cmd_args.verbose:
        RunCommand.trace_on = True

    top_commit, repo_name, local_branch_name, remote_branch_name, last_commit_sha_and_comment, last_commit_body = init()

    if not "GITHUB_TOKEN" in os.environ:
        print("Error: GITHUB_TOKEN is no exported.")
        sys.exit(1)

    token = os.environ['GITHUB_TOKEN']
    github = Github(login_or_token="access_token", password=token)

    user_name = github.get_user().login
    print("github user-name:", user_name)

    if cmd_args.org != '':
        org = github.get_organization(cmd_args.org)
        repo = org.get_repo(repo_name)
    else:
        repo = github.get_user().get_repo(repo_name)


    if cmd_args.new_pr:
        create_branch_and_pr(repo, local_branch_name, last_commit_sha_and_comment, last_commit_body)
    elif cmd_args.update_pr:
        push_state_to_branch(remote_branch_name)
    elif cmd_args.wait:
        pass
    else:
        print("Error: action not specified")
        sys.exit(1)

    status, url = wait_for_commit_to_build(repo, top_commit)
    if status:
        print("Build succeeded! url: ", url)
        beep(True)
    else:
        print("Build failed. url: ", url)
        beep(False)

    if cmd_args.showlog:
        show_build_log(url)

if __name__ == '__main__':
    main()
