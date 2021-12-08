# Overview
This is a simple script to add users in bulk to a WebEx Teams Team. 

__Note__ that this is for a ***Team*** not an individual ***Space***.

# Install
Clone (or download):  

`git clone https://github.com/ironbow/webex-teams-bulk-add.git`

Install requirements: 

`pip install -r requirements.txt`


If you need your personal token, please [visit the WebEx Teams Developer docs](https://developer.webex.com/docs/api/getting-started) while logged in to copy your Personal Access Token.
# Usage
```
usage: bulk-add.py [-h] -i IDENTITY_TOKEN -t TEAM -f FILE [-r ROOMS] [-a] [-m]

Add bulk users to WebEx Teams Team.

optional arguments:
  -h, --help            show this help message and exit
  -i IDENTITY_TOKEN, --identity_token IDENTITY_TOKEN
                        The token (or other valid token) to connect to the WebEx Teams API. This should be a moderator in the target Team. 
                        Your personal token can be found here: https://developer.webex.com/docs/api/getting-started
  -t TEAM, --team TEAM  The Team Name users should be added to.
  -f FILE, --file FILE  File that contains one user email per line.
  -r ROOMS, --rooms ROOMS
                        Specify room names that given users should be added to. Should be a quote-wrapped, semicolon-separated list of room names.
  -a, --all-rooms       Add the users to all the existing Team rooms. Ignored if '-r' flag is used.

```

# Examples
Note that the `[` and `]` are placeholders and not required when typing in your actual arguments.

## Add users to Team only
This will add all users to the Team. Users will automatically join the default Team room and no others.

```
./bulk-add -i [access-token] -t [team-to-add-to] -f [file-of-users]
```

## Add users to Team as moderators
This will add all users to the Team *as moderators*. Users will automatically join the default Team room and no others.

```
./bulk-add -i [access-token] -t [team-to-add-to] -f [file-of-users] -m
```

## Add users to all Rooms in Team
This will add users to the Team and all Rooms inside of it.
```
./bulk-add -i [access-token] -t [team-to-add-to] -f [file-of-users] -a
```

## Add users to specific Rooms in Team
This will add users to the Team and any rooms that match the provided rooms. List should be enclosed in quotation marks and semicolon-separated.

```
./bulk-add -i [access-token] -t [team-to-add-to] -f [file-of-users] -r "Room 1; Room 2; Room 3"
```

## Example output
```
$ ./bulk-add.py -t "Test Team" -f ./users.txt -r "Room 1; Room 2; Room 3" -i OWY2NWZmYjUtZmVlZS00NTM5LWFkODgtMWExNzY3NTAyOWY3MGU3NTU1MjEtMGY0_PF84_1727291e-ec55-497f-a686-f7742acfa91f
> Connected to API as Test User
> Loaded 20 total users..
> Finding Team details for Test Team
> 20 user(s) will be added the to the Test Team Team in following rooms:
        -- Room 1
        -- Room 2
        -- Room 3        
> Note:         
        If you want to add users to ALL rooms, use the '-a' flag.         
        If you want to add users to specific rooms, use the '-r' flag.         
        Users are always added to the Team's default room. This happens automatically upon joining the Team.

Are you sure you want to continue? (y/N) y
> Added user1@domain.com to Team!
> Adding user1@domain.com to room Room 1..
> Adding user1@domain.com to room Room 2..
> Adding user1@domain.com to room Room 3..
<output snipped>
> Added user20@domain.com to room Room 1..
> Added user20@domain.com to room Room 2..
> Added user20@domain.com to room Room 3..
```

# License
Licensed under the [MIT License](https://choosealicense.com/licenses/mit/).