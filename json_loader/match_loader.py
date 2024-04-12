from datetime import datetime

from competition_loader import insert_country
from sql_utils import insert_record, update_record, get_field


def update_countries(record):
    home_country = record['home_team']['country']
    away_country = record['away_team']['country']

    update_record('countries',
                  {'country_id': home_country['id']},
                  {'country_name': home_country['name']})
    update_record('countries',
                  {'country_id': away_country['id']},
                  {'country_name': away_country['name']})


def insert_teams(record, competition_id):
    home_team = record['home_team']
    away_team = record['away_team']

    if get_field('teams', 'team_id', {'team_orig_id': record['home_team']['home_team_id'],
                                      'competition_id': competition_id}) is None:
        insert_record('teams', {'team_orig_id': home_team['home_team_id'],
                                'team_name': home_team['home_team_name'],
                                'team_gender': home_team['home_team_gender'],
                                'team_group': home_team['home_team_group'],
                                'country_id': home_team['country']['id'],
                                'competition_id': competition_id
                                })

    if get_field('teams', 'team_id', {'team_orig_id': record['away_team']['away_team_id'],
                                      'competition_id': competition_id}) is None:
        insert_record('teams', {'team_orig_id': away_team['away_team_id'],
                                'team_name': away_team['away_team_name'],
                                'team_gender': away_team['away_team_gender'],
                                'team_group': away_team['away_team_group'],
                                'country_id': away_team['country']['id'],
                                'competition_id': competition_id
                                })

    if 'managers' in home_team:
        insert_managers(home_team['managers'])
        home_team_id = get_field('teams', 'team_id', {'team_orig_id': home_team['home_team_id'],
                                                      'competition_id': competition_id})
        insert_team_manager(home_team, home_team_id)
    if 'managers' in away_team:
        insert_managers(away_team['managers'])
        away_team_id = get_field('teams', 'team_id', {'team_orig_id': away_team['away_team_id'],
                                                      'competition_id': competition_id})
        insert_team_manager(away_team, away_team_id)


def insert_managers(managers):
    for manager in managers:
        country_id = manager['country']['id']
        if get_field('countries', 'country_name', {'country_id': country_id}) is None:
            insert_country({'country_id': country_id,
                            'country_name': manager['country']['name']
                            })

        insert_record('managers', {'manager_id': manager['id'],
                                   'manager_name': manager['name'],
                                   'manager_nickname': manager['nickname'],
                                   'manager_dob': manager['dob'],
                                   'country_id': manager['country']['id']
                                   })


def insert_team_manager(team, team_id):
    for manager in team['managers']:
        insert_record('team_managers', {'manager_id': manager['id'],
                                        'team_id': team_id
                                        })


def insert_competition_stage(competition_stage):
    insert_record('competition_stages', {'competition_stage_id': competition_stage['id'],
                                         'competition_stage_name': competition_stage['name']
                                         })


def insert_stadium(stadium):
    insert_record('stadiums', {'stadium_id': stadium['id'],
                               'stadium_name': stadium['name'],
                               'country_id': stadium['country']['id']
                               })


def insert_referee(referee):
    insert_record('referees', {'referee_id': referee['id'],
                               'referee_name': referee['name'],
                               'country_id': referee['country']['id']
                               })


def insert_match(record, competition_id):
    match_date = datetime.strptime(record['match_date'], "%Y-%m-%d").date()
    match_kickoff = datetime.strptime(record['kick_off'], "%H:%M:%S.%f").time()
    referee_id = record['referee']['id'] if 'referee' in record else None
    stadium_id = record['stadium']['id'] if 'stadium' in record else None

    home_team_id = get_field('teams', 'team_id', {'team_orig_id': record['home_team']['home_team_id'],
                                                  'competition_id': competition_id})
    away_team_id = get_field('teams', 'team_id', {'team_orig_id': record['away_team']['away_team_id'],
                                                  'competition_id': competition_id})

    insert_record('matches', {'match_id': record['match_id'],
                              'match_date': match_date,
                              'match_kickoff': match_kickoff,
                              'competition_id': competition_id,
                              'homeTeam_id': home_team_id,
                              'awayTeam_id': away_team_id,
                              'homeTeam_score': record['home_score'],
                              'awayTeam_score': record['away_score'],
                              'match_week': record['match_week'],
                              'competition_stage_id': record['competition_stage']['id'],
                              'stadium_id': stadium_id,
                              'referee_id': referee_id
                              })
