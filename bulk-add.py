#!/usr/bin/env python
from webexteamssdk import WebexTeamsAPI
from webexteamssdk import exceptions
import argparse


def add_users(token, team_name, users, are_moderators=False):
    # Init webexteamssdk
    api = WebexTeamsAPI(access_token=token)

    try:
        me = api.people.me()
        print(f"> Connected to API as {me.displayName}")
    except exceptions.ApiError as e:
        exit(e)

    # Load list of users to add
    print(f"> Loaded {len(users)} total users to add..")

    # Find the team by the given team name
    print(f"> Finding team details for {team_name}")
    teams = api.teams.list()
    target_team = None
    for team in teams:
        if team.name == team_name:
            target_team = team

    # If team name wasn't found.
    if not target_team:
        exit(f"The team '{team_name}' was not found in the Teams for the given token.")

    # Add users to Team
    if are_moderators:
        print("> The '-m' flag was provided. ALL users will be added as moderators.")

    for email in members_to_add:
        api.team_memberships.create(
            target_team.id, personEmail=email, isModerator=are_moderators
        )
        print(f"> Added {email} to Team!")


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
        "-m",
        "--moderator",
        help="Add the users as moderators.",
        default=False,
        action="store_true",
    )
    args = parser.parse_args()

    try:
        with open(args.file) as f:
            members_to_add = f.read().splitlines()
    except FileNotFoundError:
        exit(f"The file '{args.file}' does not exist. Please double check the path.")

    add_users(args.identity_token, args.team, members_to_add, args.moderator)
