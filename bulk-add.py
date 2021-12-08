#!/usr/bin/env python
from webexteamssdk import WebexTeamsAPI
from webexteamssdk import exceptions
import argparse
from pprint import pprint
import sys


def add_users(
    token,
    team_name,
    users,
    included_rooms=None,
    add_to_all_rooms=False,
    are_moderators=False,
    preconfirm=False,
):
    # Init webexteamssdk
    api = WebexTeamsAPI(access_token=token)

    try:
        me = api.people.me()
        print(f"> Connected to API as {me.displayName}")
    except exceptions.ApiError as e:
        if e.status_code == 401:
            exit(
                "Identity token unauthorized, please get a new Identity token from: https://developer.webex.com/docs/api/getting-started"
            )
        else:
            exit(e)

    # Load list of users to add
    print(f"> Loaded {len(users)} total users..")

    # Find the team by the given team name
    print(f"> Finding Team details for {team_name}")
    teams = api.teams.list()
    target_team = None
    for team in teams:
        if team.name == team_name:
            target_team = team

    # If team name wasn't found.
    if not target_team:
        exit(f"The Team '{team_name}' was not found in the Teams for the given token.")

    # Add users to Team
    if are_moderators:
        print("> The '-m' flag was provided. ALL users will be added as moderators.")

    # Get the rooms to add the users to based on user-provided options
    if included_rooms:
        # User gave a list of rooms, find the rooms by name (as well as the default room)
        rooms = [
            room
            for room in api.rooms.list(teamId=target_team.id)
            if (room.title in included_rooms)
        ]
    elif add_to_all_rooms:
        # User wants to add users to all rooms
        rooms = api.rooms.list(teamId=target_team.id)
    else:
        # No rooms were provided. Users will still join the default room upon joining the Team.
        rooms = []

    print(
        f"> {len(users)} user(s) will be added the to the {target_team.name} Team in following rooms:",
        *[room.title for room in rooms],
        sep="\n\t-- ",
    )
    print(
        "> Note: \
        \n\tIf you want to add users to ALL rooms, use the '-a' flag. \
        \n\tIf you want to add users to specific rooms, use the '-r' flag. \
        \n\tUsers are always added to the Team's default room. This happens automatically upon joining the Team.\n"
    )

    # Confirm with user that things look right before continuing
    if not preconfirm:
        if not input("Are you sure you want to continue? (y/N) ").lower() == "y":
            print("Aborting..")
            sys.exit(0)

    for email in members_to_add:
        # Depending on how many users you're adding, the API may rate limit the script.
        # The Teams SDK will handle that automatically, but you may see the script pause.

        # Add user to Team
        try:
            api.team_memberships.create(
                target_team.id, personEmail=email, isModerator=are_moderators
            )
            print(f"> Added {email} to Team!")
        except exceptions.ApiError as e:
            if e.response.status_code == 409:
                print(f"> {email} was already a member of the team. Skipping..")
            else:
                print(e)

        # Add user to rooms, if chosen
        for room in rooms:
            if room.isLocked:
                # "Locked" rooms are any rooms that are "moderated"
                # such as the default Team room. Let's skip them
                # to reduce unnecessary errors.
                continue
            try:
                api.memberships.create(
                    room.id, personEmail=email, isModerator=are_moderators
                )
            except exceptions.ApiError as e:
                if e.response.status_code == 409:
                    print(
                        f"> {email} was already a member of room {room.title}. Skipping.."
                    )
                else:
                    print(e)
            print(f"> Adding {email} to room {room.title}..")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add bulk users to WebEx Teams Team.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--identity_token",
        type=str,
        required=True,
        help="The token (or other valid token) to connect to the WebEx Teams API. This should be a moderator in the target Team. \nYour personal token can be found here: https://developer.webex.com/docs/api/getting-started",
    )
    parser.add_argument(
        "-t",
        "--team",
        type=str,
        required=True,
        help="The Team Name users should be added to.",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="File that contains one user email per line.",
    )
    parser.add_argument(
        "-r",
        "--rooms",
        help="Specify room names that given users should be added to. Should be a quote-wrapped, semicolon-separated list of room names.",
        default=None,
    )
    parser.add_argument(
        "-a",
        "--all-rooms",
        help="Add the users to all the existing Team rooms. Ignored if '-r' flag is used.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-m",
        "--moderator",
        help="Add the users as moderators.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--confirm",
        help="Proactively confirm script changes. This bypasses the confirmation prompt.",
        default=False,
        action="store_true",
    )
    args = parser.parse_args()

    try:
        with open(args.file) as f:
            members_to_add = f.read().splitlines()
    except FileNotFoundError:
        exit(f"The file '{args.file}' does not exist. Please double check the path.")

    if args.rooms:
        # Split the rooms by semicolons and remove surrounding spaces
        args.rooms = [room.strip() for room in args.rooms.split(";")]

    add_users(
        args.identity_token,
        args.team,
        members_to_add,
        args.rooms,
        args.all_rooms,
        args.moderator,
        args.confirm,
    )
