import requests
import datetime


def fetch_git_repositories(search_params):
    api_git_http = 'https://api.github.com/search/repositories'
    request = requests.get(api_git_http, params=search_params)
    if request.status_code == requests.codes.ok:
        return request.json()


def fetch_gitreps_created_recently(count_days_adjust):
    search_date = format_day_for_search(get_last_day(count_days_adjust))
    search_params = {'q': 'created:>={0}'.format(search_date),
                     'sort': 'stars', 'order': 'desc'}
    return fetch_git_repositories(search_params)


def get_last_day(count_days_adjust):
    today = datetime.date.today()
    return today - datetime.timedelta(days=count_days_adjust)


def format_day_for_search(search_date):
    return search_date.isoformat()


def get_trending_repositories(top_size, count_days_adjust):
    repositories = fetch_gitreps_created_recently(count_days_adjust)
    return repositories['items'][:top_size]


def print_git_repositories_short_information(repositories):
    for repos in repositories:
        print('Name: {0}'.format(repos['name']))
        print('Description: {0}'.format(repos['description']))
        print('URL: {0}'.format(repos['html_url']))
        print('Open issues amount: {0}'.format(repos['open_issues']))
        print('')


if __name__ == '__main__':
    amount_repositories = 20
    count_days = 7
    repositories = get_trending_repositories(amount_repositories, count_days)
    print_git_repositories_short_information(repositories)
