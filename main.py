"""
@Project: Schweitzer-System
@Author: MrMidnight
@Version: 6.9
"""

import random

def initialize_tournament(players):
    tournament = {player: 0 for player in players}
    return tournament


def print_round_info(round_num, tournament, watching_player):
    print(f"\nRound {round_num} - Current Points:")
    for player, points in tournament.items():
        print(f"{player}: {points} points")

    print("\nWatching:")
    print(watching_player)


def print_matchups(matchups):
    print("\nMatchups:")
    for match in matchups:
        print(f"{match[0]} vs {match[1]}")


def generate_matchups(players):
    random.shuffle(players)
    matchups = [(players[i], players[i + 1]) for i in range(0, len(players) - 1, 2)]
    return matchups


def conduct_round(round_num, tournament, matchups, watching_player):
    print_round_info(round_num, tournament, watching_player)
    print_matchups(matchups)

    input_valid = False

    while not input_valid:
        results = {}
        for match in matchups:
            winner = input(f"Enter the winner of {match[0]} vs {match[1]} (0 for {match[0]}, 1 for {match[1]}, 2 for draw): ").strip()
            if winner not in ['0', '1', '2']:
                print("Invalid input. Try again.")
                input_valid = False
            else:
                input_valid = True
                results[match] = match[int(winner)] if winner != '2' else 'draw'
                break

        # Update tournament based on results
        for match, winner in results.items():
            if winner == 'draw':
                for player in match:
                    tournament[player] += 1
            else:
                tournament[winner] += 1

    return tournament


def filter_players_by_points(tournament, points):
    return [player for player, p in tournament.items() if p == points]


def generate_next_round_matchups(tournament, previous_watching_players):
    eligible_players = set(tournament.keys()) - set(previous_watching_players)

    if len(eligible_players) < 2:
        return [], None  # No more matchups can be generated

    watching_player = random.choice(list(eligible_players))
    eligible_players.remove(watching_player)

    if len(eligible_players) % 2 != 0:
        eligible_players.add(watching_player)
        watching_player = None

    next_round_matchups = []
    unique_points = set(tournament.values())

    for points in unique_points:
        players_with_same_points = filter_players_by_points(tournament, points)
        if watching_player in players_with_same_points:
            players_with_same_points.remove(watching_player)
        next_round_matchups.extend(generate_matchups(players_with_same_points))

    random.shuffle(next_round_matchups)
    return next_round_matchups, watching_player


def main():
    print(
        " _____                                                           _   \n(_   _)                                                         ( )_ \n  | |   _    _   _  _ __   ___     _ _   ___ ___     __    ___  | ,_)\n  | | /'_`\ ( ) ( )( '__)/' _ `\ /'_` )/' _ ` _ `\ /'__`\/' _ `\| |  \n  | |( (_) )| (_) || |   | ( ) |( (_| || ( ) ( ) |(  ___/| ( ) || |_ \n  (_)`\___/'`\___/'(_)   (_) (_)`\__,_)(_) (_) (_)`\____)(_) (_)`\__)")
    print("By: MrMidnight / Version: 6.9\n")
    player_names = input("Enter player names separated by commas: ").split(',')
    tournament = initialize_tournament(player_names)

    watching_players = set()
    round_num = 1
    while True:
        matchups, watching_player = generate_next_round_matchups(tournament, watching_players)

        if not matchups:
            break  # Tournament ends when there are no more matchups to generate

        tournament = conduct_round(round_num, tournament, matchups, watching_player)
        round_num += 1
        watching_players.add(watching_player)

    print("\nTournament Complete!")
    print_round_info(round_num - 1, tournament, "None")


if __name__ == "__main__":
    main()
