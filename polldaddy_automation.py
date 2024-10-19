'''
Vote automatically on Polldaddy.com
https://github.com/wrestleraaron/polldaddy_automation
GPLv3 license
May 2024
'''
import time
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
        print(f'Failed to get cookie. Error: {err}\n {req.text}')
    end_string = req.text.index(';') - 1
    start_string = req.text.index('=') + 2

    return req.text[start_string:end_string]


def cast_vote(url: str, vote_info: dict, cookie_id: str, hdrs: str) :
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


    uri = f'{url}?p=14513898&b=0&a=64528431,&o=&va=16&cookie=0&tags=14513898-src:poll-oembed-simple&n={cookie_id}&url=https%3A//www.si.com/high-school/maryland/top-10-high-school-mascots-in-maryland-vote-for-the-best-01jabjn1jkb1'
    try:
        req = requests.get(uri, headers=hdrs, timeout=60)
        req.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f'Failed to get cookie. Error: {err}\n {req.text}')

    tester2 = req.text.__contains__('Thank you for voting!')
    #print(tester2)
    return tester2


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
    totalCount=0
    while True:
        cookie = get_cookie(COOKIE_URL, inputs, headers)
        #print(cookie)
        voteWorked = cast_vote(POLL_URL, inputs, cookie, headers)

        if voteWorked:
            #print("Good")
            time.sleep(.05)
            totalCount=totalCount+1
            print(totalCount, end=",")
        else:
            print(f'\nBlocked at {time.ctime()}. '
                  'Sleeping for 60 seconds!')
            time.sleep(60)
