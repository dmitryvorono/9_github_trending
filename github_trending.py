import requests
import datetime


def fetch_gitreps_created_last_week():
    search_date = format_day_for_search(get_last_week_day())
    search_params = {'q': 'created:>={0}'.format(search_date),
                     'sort': 'stars', 'order': 'desc'}
    r = requests.get('https://api.github.com/search/repositories',
                     params=search_params)
    if not r.raise_for_status():
        return r.json()


def get_last_week_day():
    count_days_for_adjust = 7
    today = datetime.date.today()
    return today - datetime.timedelta(days=count_days_for_adjust)


def format_day_for_search(search_date):
    return search_date.isoformat()


def get_trending_repositories(top_size):
    repositories = fetch_gitreps_created_last_week()
    return repositories['items'][:top_size]


def fetch_open_issues_amount(repo_owner, repo_name):
    r = requests.get('https://api.github.com/repos/{0}/{1}/issues'
                     .format(repo_owner, repo_name))
    if r.raise_for_status():
        return None
    return len(r.json())


def print_git_repositories_short_information(repositories):
    for repos in repositories:
        repos_owner = repos['owner']['login']
        repos_name = repos['name']
        open_issues_amount = fetch_open_issues_amount(repos_owner, repos_name)
        print('Name: {0}'.format(repos['name']))
        print('Description: {0}'.format(repos['description']))
        print('URL: {0}'.format(repos['html_url']))
        print('Open issues amount: {0}'.format(open_issues_amount))


if __name__ == '__main__':
    amount_repositories = 20
    repositories = get_trending_repositories(amount_repositories)
    print_git_repositories_short_information(repositories)
