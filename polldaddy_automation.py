import random
import sys
import time
from bs4 import BeautifulSoup
import requests
import yaml


def get_cookie(url: str, pollid: str, pollnum: str, hdrs: str) -> str:
    '''
    Fetches a cookie required for casting a vote on a Polldaddy poll.

    Args:
    url (str): The base URL for Polldaddy cookie generation.
    pollid (str): The unique identifier for the poll.
    pollnum (str): The poll number.
    hdrs (dict): A dictionary containing request headers, including a User-Agent.

    Returns:
    str: The extracted cookie value from the response.

    Raises:
    requests.exceptions.RequestException: If an error occurs during the request.
    '''
    uri = f'{url}/{pollid}/{pollnum}?{int(time.time())}'
    try:
        req = requests.get(uri, headers=hdrs)
        req.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise(f'Failed to get cookie. Error: {err}\n {req.text}')
    end_string = req.text.index(';') - 1
    start_string = req.text.index('=') + 2

    return req.text[start_string:end_string]

   
def cast_vote(url: str,
              pollnum: str,
              choice: str,
              ref_uri: str,
              cookie_id,
              hdrs: str,
              name: str) -> int:
    '''
    Casts a vote on a Polldaddy poll.

    Args:
    url (str): The base URL for Polldaddy vote casting.
    pollnum (str): The poll number.
    choice (str): The vote selection value.
    ref_uri (str): The referer URI for the vote.
    cookie_id (str): The cookie value obtained from get_cookie().
    hdrs (dict): A dictionary containing request headers, including a User-Agent.
    name (str): The display name associated with the vote.

    Returns:
    int: The current vote count for the chosen option.

    Raises:
    requests.exceptions.RequestException: If an error occurs during the request.
    UnboundLocalError: If parsing the response HTML encounters unexpected structure.
    '''
    uri = f'{url}?p={pollnum}&b=0&a={choice}'\
          f',&o=&va=16&cookie=0&tags={pollnum}-src:'\
          f'poll-embed&n={cookie_id}&url={ref_uri}'
    try:
        req = requests.get(uri, headers=hdrs)
        req.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise(f'Failed to get cookie. Error: {err}\n {req.text}')
    
    soup = BeautifulSoup(req.text, 'lxml')
    noms = soup.find_all('li')
    for _counter, info in enumerate(noms):
        if info.find('span', {'title': name}):
            try:
                votes = info.find('span', {'class': 'pds-feedback-votes'}).text.strip()
                votes = votes[1:6].replace(',','').strip() 
                pct = info.find('span', {'class': 'pds-feedback-per'}).text.strip()
                print(f'{name}: {votes}, {pct}')
            except UnboundLocalError:
                print(f"Error getting proper values. Output of error is: {noms}")
                votes = 0
    return int(votes)


def vote_data() -> dict:
    '''
    Reads vote configuration data from a YAML file.

    Returns:
    dict: A dictionary containing the necessary information to vote on Polldaddy.
    '''
    with open('poll_inputs.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return(data)


if __name__ == '__main__':
    cookie_url = 'https://polldaddy.com/n'
    poll_url = 'https://polls.polldaddy.com/vote-js.php'
    
    inputs = vote_data()
    poll_id = inputs['poll_uid']
    poll_number = inputs['poll']
    our_pick = inputs['selection']
    referer =  inputs['referer']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                            f'(KHTML, like Gecko) Chrome/{inputs['version']}.0.0.0 Safari/537.36'
              }
    vote_name = inputs['name']
    
    tally = 0
    while True:
        prev = tally
        cookie = get_cookie(cookie_url, poll_id, poll_number, headers)
        tally = cast_vote(poll_url, poll_number, our_pick, referer, cookie, headers, vote_name)
        if prev == tally:
            print(f'Total not incrementing at {time.ctime()}. Sleeping for 60 seconds!')
            time.sleep(60)
        else:
            time.sleep(5)
