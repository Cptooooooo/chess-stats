# A python module to fetch games from chess.com using their public api.
# We first get the list of monthly archives available and then fetch each 
# month's complete archive as a list of `Game`s.
# Each `Game`:dict has the following format:
"""
{
  "white": { // details of the white-piece player:
    "username": "string", // the username
    "rating": 1492, // the player's rating after the game finished
    "result": "string", // see "Game results codes" section
    "@id": "string" // URL of this player's profile
  },
  "black": { // details of the black-piece player:
    "username": "string", // the username
    "rating": 1942, // the player's rating after the game finished
    "result": "string", // see "Game results codes" section
    "@id": "string" // URL of this player's profile
  },
  "accuracies": { // player's accuracies, if they were previously calculated
    "white": float,
    "black": float
  },
  "url": "string", // URL of this game
  "fen": "string", // final FEN
  "pgn": "string", // final PGN
  "start_time": 1254438881, // timestamp of the game start (Daily Chess only)
  "end_time": 1254670734, // timestamp of the game end
  "time_control": "string", // PGN-compliant time control
  "time_class": "string", // Time class ("blitz", "rapid", "bullet")
  "rules": "string", // game variant information (e.g., "chess960")
  "eco": "string", //URL pointing to ECO opening (if available),
  "tournament": "string", //URL pointing to tournament (if available),
  "match": "string", //URL pointing to team match (if available)
}
"""

import urllib.request
import urllib.parse
from urllib.error import *
import json
import datetime

#==============================================================================
# Symbolic constants
#==============================================================================
# API Urls
archives_url = "https://api.chess.com/pub/player/%s/games/archives"
                                            #    ^^
                                            #  username

games_url = "https://api.chess.com/pub/player/%s/games/%s/%s" 
                                        #     ^^       ^^ ^^
                                        #   username   ||  |
                                        #             YYYY |
                                        #                  MM


#==============================================================================

def error(err_str):
    raise Exception(err_str)

class Games_Iter():
    """ Iterator for monthly archives """

    def __init__(self, arch_list):
        self.__arch_list = arch_list
        self.__arch_list_len = len(self.__arch_list)
        self.__index = 0

    def __iter__(self):
        return self

    def __next__(self):
        """ Fetch and return current index's games """
        if self.__index == self.__arch_list_len:
            raise StopIteration
        games = fetch_games(self.__arch_list[self.__index])
        self.__index += 1
        return games

def fetch_games(url):
    """ Fetch games from `url` and return them as a list.
        See top documentation for format of a game
    """ 
    try:
        with urllib.request.urlopen(url) as resp:
            games = json.load(resp)["games"]
            return games
    except HTTPError as e:
        print("ERROR- fetch_games: (%d) Request unsuccessful to : %s"
                % (e.code, url))
        exit(1)
    except URLError as e:
        print("ERROR- Games_Iter.next(): Failed to reach server: %s"
                % (urllib.parse.urlparse(url).hostname))

def get_arch_list(user):
    """ Get a list of monthly archives available for `user`. The list is an 
        array of urls to fetch each month's games from.
    """
    try:
        url = archives_url % user
        with urllib.request.urlopen(url) as resp:
            return json.load(resp)["archives"]
    except HTTPError as e:
        print("ERROR- get_arch_list(): (%d) Request unsuccessful to : %s"
                % (e.code, url))
        exit(1)
    except URLError as e:
        print("ERROR- Games_Iter.next(): Failed to reach server: %s"
                % (urllib.parse.urlparse(url).hostname))

def limit_arch_list(arch_list, start=None, end=None, excludes=[]):
    """ Limit the archive list to months between start and end and return a 
        new list. Excludes months in `excludes`.
    """
    if start == None and end == None:
        return arch_list.copy()

    l_arch_list = []
    # if start > end, return []
    if (start and end) and (start > end):
        return l_arch_list

    for url in arch_list:
        _, year, month = url.rsplit("/", 2)
        year = int(year)
        month = int(month)

        dt = datetime.datetime(year, month, 1)
        if dt in excludes:
            continue
        if start != None and (dt < start):
            continue
        if end != None and (dt > end):
            continue

        l_arch_list.append(url)

    return l_arch_list

def get_all_games(user, start=None, end=None, excludes=[]):
    """ Returns an iterator to iterate over each month's game between start 
        and end time period excluding months in `excludes`.
    """
    arch_list = get_arch_list(user)
    if start or end:
        arch_list = limit_arch_list(arch_list, start, end, excludes)
    return Games_Iter(arch_list)

def get_month_games(user:str, month:int, year:int):
    try:
        date = datetime.date(year, month, 1)
    except ValueError as e:
        print("ERROR get_month_games():", e)

    month = date.strftime("%m")
    year = date.strftime("%Y")

    return fetch_games(games_url % (user, year, month))

if __name__ == "__main__":

    for month_games in get_all_games("cptooooooooo"):
        print(json.dumps(month_games))

