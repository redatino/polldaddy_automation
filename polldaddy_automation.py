'''
Vote automatically on Polldaddy.com
'''
import time
from bs4 import BeautifulSoup
import requests
import yaml

COOKIE_URL = 'https://polldaddy.com/n'
POLL_URL = 'https://polls.polldaddy.com/vote-js.php'


def get_cookie(url: str, vote_info: dict, hdrs: str) -> str:
    '''
    Fetches a cookie required for casting a vote on a Polldaddy poll.

    Args:
    url (str): The base URL for Polldaddy cookie generation.
    vote_info (dict): Necessary information for casting correct vote
    hdrs (dict): A dictionary containing request headers, including User-Agent.

    Returns:
    str: The extracted cookie value from the response.

    Raises:
    requests.exceptions.RequestException: If an error occurs during the request
    '''
    pollid = vote_info['poll_uid']
    pollnum = vote_info['poll']

    uri = f'{url}/{pollid}/{pollnum}?{int(time.time())}'
    try:
        req = requests.get(uri, headers=hdrs, timeout=60)
        req.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise f'Failed to get cookie. Error: {err}\n {req.text}'
    end_string = req.text.index(';') - 1
    start_string = req.text.index('=') + 2

    return req.text[start_string:end_string]


def cast_vote(url: str, vote_info: dict, cookie_id: str, hdrs: str) -> int:
    '''
    Casts a vote on a Polldaddy poll.

    Args:
    url (str): The base URL for Polldaddy vote casting.
    vote_info (dict): Necessary information for casting correct vote
    cookie_id (str): The cookie value obtained from get_cookie().

    Returns:
    int: The current vote count for the chosen option.

    Raises:
    requests.exceptions.RequestException: If an error occurs during the request
    UnboundLocalError: If response HTML encounters unexpected HTML structure.
    '''
    name = vote_info['name']

    uri = f'{url}?p={vote_info['poll']}&b=0&a={vote_info['selection']}'\
          f',&o=&va=16&cookie=0&tags={vote_info['poll']}-src:'\
          f'poll-embed&n={cookie_id}&url={vote_info['referer']}'
    try:
        req = requests.get(uri, headers=hdrs, timeout=60)
        req.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise f'Failed to get cookie. Error: {err}\n {req.text}'
    votes = 0
    soup = BeautifulSoup(req.text, 'lxml')
    noms = soup.find_all('li')
    for _counter, info in enumerate(noms):
        if info.find('span', {'title': name}):
            try:
                votes = info.find('span', {'class': 'pds-feedback-votes'}).text.strip()
                space = votes.find(' ')
                votes = votes[1:space].replace(',', '').strip()
                pct = info.find('span', {'class': 'pds-feedback-per'}).text
                print(f'{name}: {votes}, {pct}')
            except UnboundLocalError:
                print(f"Error getting proper values. Resetting votes to 0")
    return int(votes)


def vote_data() -> dict:
    '''
    Reads vote configuration data from a YAML file.

    Returns:
    dict: A dictionary containing the needed information to vote on Polldaddy.
    '''
    with open('poll_inputs.yaml', 'r', encoding='utf-8') as fp:
        data = yaml.load(fp, Loader=yaml.SafeLoader)
    return data


if __name__ == '__main__':
    inputs = vote_data()
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                f'{inputs["version"]}.0.0.0 Safari/537.36'
              }

    tally = 0
    while True:
        prev = tally
        cookie = get_cookie(COOKIE_URL, inputs, headers)
        tally = cast_vote(POLL_URL, inputs, cookie, headers)
        if prev == tally:
            print(f'Total not incrementing at {time.ctime()}. '
                  'Sleeping for 60 seconds!')
            time.sleep(60)
        else:
            time.sleep(5)
