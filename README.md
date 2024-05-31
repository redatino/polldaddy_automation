# polldaddy_automation

This project is a python function (with a Windows executable) that allows for automated voting on polldaddy.com. Required information is: poll uniqueid, poll number, selection id number, referer, and full name of the selection. 

The information is updated in poll_inputs.yaml which needs to be stored in the same directory as the python script or executable.

As of May 2024 there is rate limiting at polldaddy to prevent too many votes from being submitted. It appeared to be based on IP address, and the 60 second wait is required when the rate limit is hit and the vote does not increment



## Badges

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)



## Authors

- [@wrestleraaron](https://www.github.com/wrestleraaron)


## Acknowledgements

 - [@kingbin - polldaddy.rb](https://gist.github.com/kingbin/1690064)
