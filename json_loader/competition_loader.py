from sql_utils import insert_record


def insert_country(record):
    if 'country_id' in record:
        insert_record('countries', {'country_id': record['country_id'],
                                    'country_name': record['country_name']
                                    })
    else:
        insert_record('countries', {'country_name': record['country_name']
                                    })


def insert_competition(record):
    competition_youth = record['competition_youth'] == 'true'
    competition_international = record['competition_international'] == 'true'

    insert_record('competitions_seasons', {'competition_orig_id': record['competition_id'],
                                           'season_id': record['season_id'],
                                           'season_name': record['season_name'],
                                           'competition_name': record['competition_name'],
                                           'competition_gender': record['competition_gender'],
                                           'competition_youth': competition_youth,
                                           'competition_international': competition_international,
                                           'country_name': record['country_name']
                                           })
