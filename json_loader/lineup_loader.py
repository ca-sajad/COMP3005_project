"""Loads data from a json file in open-data/data/lineups folder into the database"""
from .competition_loader import insert_country
from .sql_utils import insert_record, get_field


def insert_lineup(competition_id, match_id, record):
    """Uses helper functions to add a team's players data to db

    :param competition_id: an integer representing the id of the competition the team has participated in
    :param match_id: an integer representing the id of a match the team is part of
    :param record: an entry in a json file in the 'lineups' folder
    :return: None
    """
    team_id = get_field('teams', 'team_id', {'team_orig_id': record['team_id'],
                                             'competition_id': competition_id
                                             })
    for player in record['lineup']:
        # add player to players and lineups tables
        insert_player_lineup(competition_id, team_id, match_id, player)
        # add player to player_match_position table
        insert_player_match_position(team_id, match_id, player)
        # add player to player_match_cards table
        insert_player_match_card(team_id, match_id, player)


def insert_player_lineup(competition_id, team_id, match_id, player):
    """Inserts into 'players', 'player_jerseys', and 'lineups' tables of db

    :param competition_id: an integer representing the id of the competition the team has participated in
    :param team_id: an integer representing the id of a "home_team" or "away_team"
    :param match_id: an integer representing the id of a match the team is part of
    :param player: an element in the "lineup" array of an entry in a json file in the 'lineups' folder
    :return: None
    """
    country_id = player['country']['id']
    if get_field('countries', 'country_name', {'country_id': country_id}) is None:
        insert_country({'country_id': country_id,
                        'country_name': player['country']['name']
                        })

    insert_record('players', {'player_id': player['player_id'],
                              'player_name': player['player_name'],
                              'player_nickname': player['player_nickname'],
                              'country_id': player['country']['id']
                              })
    insert_record('player_jerseys', {'player_id': player['player_id'],
                                     'jersey_number': player['jersey_number'],
                                     'competition_id': competition_id
                                     })
    insert_record('lineups', {'match_id': match_id,
                              'team_id': team_id,
                              'player_id': player['player_id']
                              })


def insert_player_match_position(team_id, match_id, player):
    """Inserts into 'player_match_positions' table of db

    :param team_id: an integer representing the id of a "home_team" or "away_team"
    :param match_id: an integer representing the id of a match the team is part of
    :param player: an element in the "lineup" array of an entry in a json file in the 'lineups' folder
    :return: None
    """
    positions = player['positions']
    for position in positions:

        time_from, time_to = None, None
        if position['from'] is not None:
            time_from = position['from']
        if position['to'] is not None:
            time_to = position['to']

        player_position_id = position['position_id']
        if get_field('player_positions', 'player_position_name',
                     {'player_position_id': player_position_id}) is None:
            insert_player_position(position)

        insert_record('player_match_positions', {'match_id': match_id,
                                                 'team_id': team_id,
                                                 'player_id': player['player_id'],
                                                 'player_position_id': position['position_id'],
                                                 'time_from': time_from,
                                                 'time_to': time_to,
                                                 'from_period': position['from_period'],
                                                 'to_period': position['to_period'],
                                                 'start_reason': position['start_reason'],
                                                 'end_reason': position['end_reason']
                                                 })


def insert_player_position(position):
    """Inserts into 'player_positions' table of db

    :param position: an element in the "player_positions" array of an entry in a json file in the 'lineups' folder
    :return: None
    """
    insert_record('player_positions', {'player_position_id': position['position_id'],
                                       'player_position_name': position['position']
                                       })


def insert_player_match_card(team_id, match_id, player):
    """Inserts into 'player_match_cards' table of db

    :param team_id: an integer representing the id of a "home_team" or "away_team"
    :param match_id: an integer representing the id of a match the team is part of
    :param player: an element in the "lineup" array of an entry in a json file in the 'lineups' folder
    :return: None
    """
    cards = player['cards']

    for card in cards:
        time = card.get('time')

        insert_record('player_match_cards', {'match_id': match_id,
                                             'team_id': team_id,
                                             'player_id': player['player_id'],
                                             'time': time,
                                             'card_type': card['card_type'],
                                             'reason': card['reason'],
                                             'period': card['period']
                                             })
