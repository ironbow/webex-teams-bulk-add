# Overview
This is a simple script to add users in bulk to a WebEx Teams Team. 

__Note__ that this is for a ***Team*** not an individual ***Space***.

# Install
Clone (or download):  

`git clone https://github.com/ironbow/webex-teams-bulk-add.git`

Install requirements: 

`pip install -r requirements.txt`

Run:

`./bulk-add -i [access-token] -t [team-to-add-to] -f [file-of-users]`

If you want to add the users as moderators, add `-m`:

`./bulk-add -i [access-token] -t [team-to-add-to] -f [file-of-users] -m`

If you need your personal token, please [visit the WebEx Teams Developer docs](https://developer.webex.com/docs/api/getting-started) while logged in to copy your Personal Access Token.
# Usage
```
usage: bulk-add.py [-h] -i IDENTITY_TOKEN -t TEAM -f FILE [-a] [-m]

Add bulk users to WebEx Teams Team.

optional arguments:
  -h, --help            show this help message and exit
  -i IDENTITY_TOKEN, --identity_token IDENTITY_TOKEN
                        The token (or other valid token) to connect to the WebEx Teams API. This should be a moderator in the target Team. 
                        Your personal token can be found here: https://developer.webex.com/docs/api/getting-started
  -t TEAM, --team TEAM  The Team Name users should be added to.
  -f FILE, --file FILE  File that contains one user email per line.
  -a, --all-rooms       Add the users to all the existing Team rooms.
  -m, --moderator       Add the users as moderators.
```

# License
Licensed under the [MIT License](https://choosealicense.com/licenses/mit/).