
import os
import json
from constants import *
from competition_loader import *
from match_loader import *
from lineup_loader import *
from event_loader import *


def find_file(start_dir, target_file):
    for root, dirs, files in os.walk(start_dir):
        if target_file in files:
            return os.path.join(root, target_file)
    return None


def load_competition(competition_name, season_name):
    competition_file_path = find_file(BASE_PATH, COMPETITION_FILE_NAME)

    with open(competition_file_path, 'r') as file:
        competition_data = json.load(file)

    for record_1 in competition_data:
        if record_1['competition_name'].lower() == competition_name.lower() and \
                record_1['season_name'].lower() == season_name:
            # loading competition
            insert_country(record_1)
            insert_competition(record_1)

            competition_id = get_field('competitions_seasons', 'competition_id',
                                       {'competition_orig_id': record_1['competition_id'],
                                        'season_id': record_1['season_id']
                                        })

            # loading matches
            matches_dir = os.path.join(MATCHES_PATH, str(record_1['competition_id']))
            matches_file = find_file(matches_dir, str(record_1['season_id']) + ".json")
            with open(matches_file, 'r') as file:
                matches_data = json.load(file)

            for record_2 in matches_data:
                update_countries(record_2)
                insert_teams(record_2, competition_id)
                insert_competition_stage(record_2['competition_stage'])
                if 'stadium' in record_2:
                    insert_stadium(record_2['stadium'])
                if 'referee' in record_2:
                    insert_referee(record_2['referee'])
                insert_match(record_2, competition_id)

                match_id = record_2['match_id']

                # loading lineups
                lineups_file = find_file(LINEUPS_PATH, str(match_id) + ".json")
                with open(lineups_file, 'r') as file:
                    lineup_data = json.load(file)

                for record_3 in lineup_data:
                    insert_lineup(competition_id, match_id, record_3)

                # loading events
                events_file = find_file(EVENTS_PATH, str(match_id) + ".json")
                with open(events_file, 'r') as file:
                    events_data = json.load(file)

                for record_4 in events_data:
                    insert_event(competition_id, match_id, record_4)



