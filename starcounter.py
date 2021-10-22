#!/usr/bin/env python3

import os
import sys
import pickle
import datetime
from pathlib import Path
import argparse
from github import Github

if not "GITHUB_TOKEN" in os.environ:
    print("Error: GITHUB_TOKEN is no exported.")
    sys.exit(1)

class Data:
    def __init__(self, entries = None, date = None):

        if entries is None:
            self.entries = []
        else:
            self.entries = entries

        if  date is None:
            date = datetime.datetime.now()
        self.date = date

class Entry:
    def __init__(self, stars, name):
        self.stars = stars
        self.name = name

def show_diff_old_new(entries, old_data):
    if old_data is None:
        return

    print("old_date: ", old_data.date, "now:", datetime.datetime.now())

    old_entries = old_data.entries
    for entry in entries:
        shown_entry = True
        for old_entry in old_entries:
            if entry.name == old_entry.name:
                if entry.stars != old_entry.stars:
                    print(entry.name, "stars changed from:", old_entry.stars, "to:", entry.stars)
                    shown_entry = False
                    break
        if not shown_entry:
            print(entry.name, "new project. stars:", entry.stars)



def diff_it(entries, old_data):
    old_entries  = old_data.entries
    if len(old_entries) != len(entries):
        return True

    for entry in entries:
        for old_entry in old_entries:
            if entry.name == old_entry.name:
                if entry.stars != old_entry.stars:
                    return True

    return False


def compare_with_previous_record(entries):
    data_file = Path(__file__).with_name('starcounter.data')

    save_it = False
    old_data = None

    if os.path.exists(data_file):
        old_data = None
        with open(data_file, 'rb') as pickle_file:
            old_data = pickle.load(pickle_file)

        if old_data is not None:
            if diff_it(entries, old_data):
                save_it = True
    else:
        save_it = True

    if save_it:
        show_diff_old_new( entries, old_data)

        with open(data_file, 'wb') as pickle_file:
            pickle.dump( Data(entries), pickle_file)


def show_repo_stars(user):
    all_stars = 0

    entries=[]
    for repo in user.get_repos():
        #print("name:", repo.name, "stars:", repo.stargazers_count)
        entries.append(Entry(repo.stargazers_count, repo.name))
        all_stars += repo.stargazers_count

    def by_stars(ent):
        return ent.stars

    entries.sort(key=by_stars, reverse=True)

    for entry in entries:
        print("name:", entry.name, "stars: ", entry.stars)

    print("***")
    print("total stars: ", all_stars)

    compare_with_previous_record(entries)

class RepoTraffic:
    def __init__(self, name, traffic_stats):
        self.name = name
        self.views_total =  int(traffic_stats['count'])
        self.views_unique =  int(traffic_stats['uniques'])
        self.all_stats = traffic_stats['views']


    def show(self):
        print("repo:", self.name, "views: total:", self.views_total, "unique: ", self.views_unique)
        for view in self.all_stats:
            print("\t", view.timestamp, "total:", view.count, "unique:", view.uniques)


def show_repo_traffic(user,stat_time):

    print("""
Traffic report
""")

    entries=[]
    for repo in user.get_repos():
        traffic = repo.get_views_traffic()
        traffic_stats = repo.get_views_traffic(per=stat_time) # default: per week

        traffic = RepoTraffic(repo.name, traffic_stats)
        entries.append(traffic)

    def by_stars(ent):
        return ent.views_total

    entries.sort(key=by_stars, reverse=True)

    for entry in entries:
        entry.show()

def parse_cmd_line():

    usage = '''
shows number of star of project owned by current github user and usage statistics

This program assumes that the environment GITHUB_TOKEN is exported, and that it has the token of the current user.
It also compares the number of stars against the previous state, and reports any difference. The new state is then stored in the starcounter.data file.
This program assumes the github api to be installed - pip install python-github-api'''

    parse = argparse.ArgumentParser(description=usage, \
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    group = parse.add_argument_group("view github data on current users repositories")

    group.add_argument('--show-stars', '-s',  default=True, \
            action='store_true', dest='show_stars', help='show stars')

    group.add_argument('--show-views', '-v',  default=False, \
            action='store_true', dest='show_views', help='show views')

    group.add_argument('--stats-time', '-t',  default='week', \
            type=str, dest='stat_time', help='time resulution of views (for --show-views)')


    return parse.parse_args(), parse


def main():
    cmd_args, _ = parse_cmd_line()

    token = os.environ['GITHUB_TOKEN']
    github = Github(login_or_token="access_token", password=token)
    user = github.get_user()
    if cmd_args.show_stars:
        show_repo_stars(user)
    if cmd_args.show_views:
        show_repo_traffic(user, cmd_args.stat_time)
main()
