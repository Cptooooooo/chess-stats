# Main Python program for fetching game data from chess.com and computing
# Performance data for plotting. It outputs the performance - 'perf of the day'
# data to perf.dat file

import fetch_games
import datetime

#==============================================================================
# Symbolic constants
#==============================================================================
# Time Zones 
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
MST = datetime.timezone(-datetime.timedelta(hours=7))
MDT = datetime.timezone(-datetime.timedelta(hours=6))

# Games
# Time classes
time_classes = ["blitz", "bullet", "rapid"]


#==============================================================================

def get_rating(user, game):
    """ Returns the rating of `user` from a game dict. If user is not in the
        game, returns None.
    """
    if game["white"]["username"].lower() == user.lower():
        return game["white"]["rating"]
    elif game["black"]["username"].lower() == user.lower():
        return game["black"]["rating"]
    else:
        return None

def epoch_to_hour(ts, tz=datetime.timezone.utc):
    """ Convert POSIX timestamp to hour of the day in timezone tz"""
    dt = datetime.datetime.fromtimestamp(ts, tz)
    return dt.hour

def avg_delta_rating(user, start=None, end=None, tz=datetime.timezone.utc, 
                        excludes=[]):
    """ Loop over games played in a time period and compute avg delta(rating) 
         per game for each hour of the day for each time format (rapid, blitz, 
         bullet).
        - user : (str) username
        - start : (datetime.datetime) Start of time period
        - end : (datetime.datetime) End of time period
        - tz : (datetime.timezone) Timezone the games were played in
        - excludes: (datetime.datetime[]) List of months to excludes
    """

    last_rating = { t_class: -1 for t_class in time_classes }

                           #  (net_rat_gain[24], n_games[24])
    rating_stats = { t_class: ([0]*24, [0]*24) for t_class in time_classes }

    for month_games in fetch_games.get_all_games(user, start, end, excludes):
        for game in month_games:
            h = epoch_to_hour(game["end_time"], tz)

            time_class = game["time_class"]
            if time_class not in time_classes:
                continue

            usr_rating = get_rating(user, game)
            if last_rating[time_class] == -1:
                last_rating[time_class] = usr_rating
                continue

            rating_stats[time_class][0][h] += (usr_rating - 
                                                last_rating[time_class])
            rating_stats[time_class][1][h] += 1

            last_rating[time_class] = usr_rating

    avg = { t_class: [0]*24 for t_class in time_classes }

    for i in range(24):
        for t_class in time_classes:
            if rating_stats[t_class][1][i]:
                avg[t_class][i] = (rating_stats[t_class][0][i] / 
                                    rating_stats[t_class][1][i])

    return avg

def write_perf_to_file(filename, perf_data):
    """ Writes performance-hour_of_the_day data for all timeclasses in order 
        (blitz, bullet, rapid).
    """

    with open(filename, 'w') as f:

        for t_class in time_classes:
            for h in range(24):
                f.write("%d %f\n" % ((h+1), perf_data[t_class][h]))
            f.write("\n\n")

if __name__ == "__main__":
    user = "cptooooooooo"

    # Timezone Switch from IST to MST
    switch_dt = datetime.datetime(2022, 8, 17)

    # Months to exclude from computation
    excludes = [datetime.datetime(2022, 8, 1)] # August, 2022

    avg_in_IST = avg_delta_rating(user, None, switch_dt, IST, excludes)
    avg_in_MST = avg_delta_rating(user, switch_dt, None, MST, excludes)

    avg = { t_class: [0]*24 for t_class in time_classes }
    for i in range(24):
        for t_class in time_classes:
            avg[t_class][i] = ((avg_in_IST[t_class][i] + 
                                avg_in_MST[t_class][i]) / 2)

    write_perf_to_file("perf.dat", avg)
