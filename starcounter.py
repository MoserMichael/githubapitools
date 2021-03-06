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

class Tab:
    tab_ = "\t"

    @staticmethod
    def set_tab(tab):
        Tab.tab_ = tab

    @staticmethod
    def get_tab(num=1):
        return Tab.tab_ * num

class Data:
    def __init__(self, entries=None, date=None):

        if entries is None:
            self.entries = []
        else:
            self.entries = entries

        if date is None:
            date = datetime.datetime.now()
        self.date = date


class Entry:
    def __init__(self, repo):
        self.stars = repo.stargazers_count
        self.name = repo.name
        self.html_url = repo.html_url
        self.language = repo.language
        self.description = repo.description



def show_diff_old_new(entries, old_data):
    if old_data is None:
        return

    print("old_date: ", old_data.date, "now:", datetime.datetime.now())

    old_entries = old_data.entries
    for entry in entries:
        entry_present = False
        for old_entry in old_entries:
            if entry.name == old_entry.name:
                entry_present = True
                if entry.stars != old_entry.stars:
                    print(
                        entry.name,
                        "stars changed from:",
                        old_entry.stars,
                        "to:",
                        entry.stars,
                    )
                    break
        if not entry_present:
            print(entry.name, "new project. stars:", entry.stars)


def diff_it(entries, old_data):
    old_entries = old_data.entries
    if len(old_entries) != len(entries):
        return True

    for entry in entries:
        for old_entry in old_entries:
            if entry.name == old_entry.name:
                if entry.stars != old_entry.stars:
                    return True

    return False


def compare_with_previous_record(entries):
    data_file = Path(__file__).with_name("starcounter.data")

    save_it = False
    old_data = None

    if os.path.exists(data_file):
        old_data = None
        with open(data_file, "rb") as pickle_file:
            old_data = pickle.load(pickle_file)

        if old_data is not None:
            if diff_it(entries, old_data):
                save_it = True
    else:
        save_it = True

    if save_it:
        show_diff_old_new(entries, old_data)

        with open(data_file, "wb") as pickle_file:
            pickle.dump(Data(entries), pickle_file)


def show_repo_stars(user, html_format):
    all_stars = 0

    entries = []
    for repo in user.get_repos():
        # print("name:", repo.name, "stars:", repo.stargazers_count)
        entries.append(Entry(repo))
        all_stars += repo.stargazers_count

    def by_stars(ent):
        return ent.stars

    entries.sort(key=by_stars, reverse=True)

    if html_format:
        Tab.set_tab("&nbsp;&nbsp;&nbsp;&nbsp;")
        print("<table><tr><th align='left'>Name</th><th align='left'>Stars</th><th align='left'>Language</th><th align='left'>description</th></tr>")


    for entry in entries:
        if not html_format:
            print("name:", entry.name, "stars: ", entry.stars)
        else:
            print(f'<tr><td><a href="{entry.html_url}">{entry.name}</a></td><td>{entry.stars}</td><td>{entry.language}</td><td>{entry.description}</td></tr>')

    if html_format:
        print("<tr><th>Total stars:</th><th colspan='2' align='left'>", all_stars, "</th></tr>")
        print("</table>")
        print("<br>")
    else:
        print("***")
        print("total stars: ", all_stars)

    compare_with_previous_record(entries)

def show_stars_sum(user):
    all_stars = 0
    for repo in user.get_repos():
        all_stars += repo.stargazers_count
    print("Sum of all stars:", all_stars)

class RepoTraffic:
    def __init__(self, name, traffic_stats, referrers):
        self.name = name
        self.views_total = int(traffic_stats["count"])
        self.views_unique = int(traffic_stats["uniques"])
        self.all_stats = traffic_stats["views"]
        self.referrers = referrers

    def show(self):
        print(
            "repo:",
            self.name,
            "views: total:",
            self.views_total,
            "unique: ",
            self.views_unique,
        )
        if len(self.all_stats) != 0:
            print("Views:")
            for view in self.all_stats:
                print(Tab.get_tab(), view.timestamp, "total:", view.count, "unique:", view.uniques)

            if len(self.referrers) != 0:
                print(Tab.get_tab() + "Referrers:")
                for referrer in self.referrers:
                    print(Tab.get_tab(2) + f"Count: {referrer.count} Unique: {referrer.uniques} Url: {referrer.referrer}")

        print("")
        return self.views_total


def show_repo_traffic(user, stat_time):

    print(f"\nTraffic report for user {user.name}\n\n")

    entries = []
    for repo in user.get_repos():
        traffic = repo.get_views_traffic()
        traffic_stats = repo.get_views_traffic(per=stat_time)  # default: per week
        referrers = repo.get_top_referrers()
#
        traffic = RepoTraffic(repo.name, traffic_stats, referrers)
        entries.append(traffic)

    def by_stars(ent):
        return ent.views_total

    entries.sort(key=by_stars, reverse=True)

    views_total = 0
    for entry in entries:
        views_total += entry.show()
    print("\n***\nTotal views:", views_total)

def get_starred_by_user(user, html_format):

    if html_format:
        print("<table><tr><th align='left'>Starred Repo</a></th align='left'><th align='left'>Language</th><th>Description of starred repo</th></tr>")
    else:
        print(f"\n\n Repositories starred by the user {user.name}\n\n")

    for repo in user.get_starred():
        if not html_format:
            print("repo:", repo.name,  "url:", repo.html_url, "description:", repo.description)
        else:
            print(f"<tr><td><a href=\"{repo.html_url}\">{repo.name}</a></td><td>{repo.language}</th><td>{repo.description}</td></tr>")
    if html_format:
        print("</table>")

def follow_everyone(user):
    added_to_following = 0
    for repo in user.get_repos():
        #print("name:", repo.name, "stars:", repo.stargazers_count)
        for starrer in repo.get_stargazers():
            if starrer.login != user.login:
                if not user.has_in_following(starrer):
                    print(f"Adding user {starrer.name} {repr(starrer)} who starrred repo {repo.name} to set of followed users")
                    user.add_to_following(starrer)
                    added_to_following += 1
    #            else:
    #                print(f"User {starrer.name} is already beeing followed")

    print("---")
    print(f"added {added_to_following} users to following")


def parse_cmd_line():
    usage = """
shows number of star of project owned by current github user and usage statistics

This program assumes that the environment GITHUB_TOKEN is exported, and that it has the token of the current user.
It also compares the number of stars against the previous state, and reports any difference. The new state is then stored in the starcounter.data file.
This program assumes the github api to be installed - pip install python-github-api"""

    parse = argparse.ArgumentParser(
        description=usage, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    group = parse.add_argument_group("view github data on current users repositories")

    group.add_argument(
        "--show-stars",
        "-s",
        default=False,
        action="store_true",
        dest="show_stars",
        help="show user's repositories and sort by stars"
    )

    group.add_argument(
        "--show-views",
        "-v",
        default=False,
        action="store_true",
        dest="show_views",
        help="show views",
    )

    group.add_argument(
        "--stats-time",
        "-t",
        default="week",
        type=str,
        dest="stat_time",
        help="time resulution of views (for --show-views)",
    )

    group.add_argument(
        "--show-user-starred",
        "-r",
        default=False,
        action="store_true",
        dest="show_starred_by_user",
        help="show repositories that the user has given a star too"
    )

    group.add_argument(
        "--html-links",
        "-l",
        default=False,
        action='store_true',
        dest="html_format",
        help="project names as html links",
    )

    group = parse.add_argument_group("follow every user who gave a star on a project"
            )

    group.add_argument(
        "--follow-everyone",
        "-f",
        default=False,
        action="store_true",
        dest="follow_everyone",
        help="follow every user who gave a star on a project"
    )

    return parse.parse_args(), parse


def main():
    cmd_args, _ = parse_cmd_line()

    token = os.environ["GITHUB_TOKEN"]
    github = Github(login_or_token="access_token", password=token)
    user = github.get_user()

    if cmd_args.show_stars:
        show_repo_stars(user, cmd_args.html_format)

    if cmd_args.show_views:
        show_repo_traffic(user, cmd_args.stat_time)

    if cmd_args.show_starred_by_user:
        get_starred_by_user(user, cmd_args.html_format)

    if cmd_args.follow_everyone:
        follow_everyone(user)

main()
