
# polldaddy_automation

This project is a python function (with a Windows executable) that allows for automated voting on polldaddy.com. Required information is: poll uniqueid, poll number, selection id number, referer, and full name of the selection. 

The information is updated in poll_inputs.yaml which needs to be stored in the same directory as the python script or executable.

As of May 2024 there is rate limiting at polldaddy to prevent too many votes from being submitted. It appeared to be based on IP address, and the 60 second wait is required when the rate limit is hit and the vote does not increment


## Known Issues

Occassionally the HTML returned from polldaddy.com will not parse correctly and cause a failure. This is a temporary error and restarting the application usually resolves this, but it does need to be monitored.

## Badges

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)



## Authors

- [@wrestleraaron](https://www.github.com/wrestleraaron)


## Run Locally

Clone the project

```bash
  git clone https://github.com/wrestleraaron/https://github.com/wrestleraaron/polldaddy_automation
```

Go to the project directory

```bash
  cd polldaddy_automation
```

Optional create a virtual python environment and activate it:

```bash
python -m venv venv
. venv/activate (Unix/Mac)
venv\scripts\activate (Windows)
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Update the poll_inputs.yaml file with the necessary and correct information. Using a browser, use Developer tools (or "Inspect page) and looking under the "Sources" tab for "secure.polldaddy.com" and getting the path and pollnumber.js file (e.g. [https://secure.polldaddy.com/p/13808984.js](https://secure.polldaddy.com/p/13808983.js)). The "var PDV_h<pollnumber> is the unique poll id.

Run the application as a standalone executable:
```bash
  polldaddy_automation.exe
```
Or via python:
```bash
  python polldaddy_automation.py
```

## Acknowledgements

 - [@kingbin - polldaddy.rb](https://gist.github.com/kingbin/1690064)
