import requests
import datetime
import json
import pprint


def fetch_gitreps_created_last_week():
    search_date = format_day_for_search(get_last_week_day())
    search_params = {'q': 'created:>={0}'.format(search_date), 'sort': 'stars', 'order': 'desc'}
    r = requests.get('https://api.github.com/search/repositories', params=search_params)
    if not r.raise_for_status():
        return r.json()


def get_last_week_day():
    count_days_for_adjust = 7
    today = datetime.date.today()
    return today - datetime.timedelta(days = count_days_for_adjust)


def format_day_for_search(search_date):
    return search_date.isoformat()


def get_trending_repositories(top_size):
    repositories = fetch_gitreps_created_last_week()
    return repositories['items'][:top_size]


def get_open_issues_amount(repo_owner, repo_name):
    pass

if __name__ == '__main__':
    pprint.pprint(len(get_trending_repositories(20)))
