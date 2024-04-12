from lineup_loader import insert_player_position
from sql_utils import insert_record, update_record, get_field


def insert_event(competition_id, match_id, record):
    event_type_id = record['type']['id']

    # don't add these types: Starting XI, Half Start, Half End, Tactical Shift, Referee Ball-Drop, Own Goal For
    if event_type_id in [35, 18, 34, 36, 41, 25]:
        return

    print(record)

    insert_play_pattern(record['play_pattern'])

    player_position_id = record['position']['id']
    if get_field('player_positions', 'player_position_name', {'player_position_id': player_position_id}) is None:
        insert_player_position({'position_id': player_position_id,
                                'position': record['position']['name']
                                })

    event_type = record['type']['name']
    if event_type not in ['Pass', 'Shot']:

        event_db_id = record['id']
        related_events = record.get('related_events', [])
        insert_related_events(related_events, event_db_id)

        location_x, location_y = None, None
        if 'location' in record:
            location_x = record['location'][0]
            location_y = record['location'][1]

        duration = record.get('duration', 0)
        under_pressure = record.get('under_pressure')
        counterpress = record.get('counterpress')

        team_id = get_field('teams', 'team_id', {'team_orig_id': record['team']['id'],
                                                 'competition_id': competition_id
                                                 })
        possession_team_id = get_field('teams', 'team_id', {'team_orig_id': record['possession_team']['id'],
                                                            'competition_id': competition_id
                                                            })

        insert_record('events', {'event_db_id': record['id'],
                                 'index': record['index'],
                                 'match_id': match_id,
                                 'team_id': team_id,
                                 'player_id': record['player']['id'],
                                 'period': record['period'],
                                 'minute': record['minute'],
                                 'second': record['second'],
                                 'event_type_name': event_type,
                                 'possession_count': record['possession'],
                                 'possession_team_id': possession_team_id,
                                 'play_pattern_id': record['play_pattern']['id'],
                                 'player_position_id': player_position_id,
                                 'location_x': location_x,
                                 'location_y': location_y,
                                 'duration': duration,
                                 'under_pressure': under_pressure,
                                 'counterpress': counterpress
                                 })

        event_id = get_field('events', 'event_id', {'event_db_id': event_db_id})

        if event_type == 'Ball Receipt*':
            insert_ball_receipt(record, event_id)

        elif event_type == 'Carry':
            insert_ball_carry(record, event_id)

        elif event_type == 'Ball Recovery':
            insert_ball_recovery(record, event_id)

        elif event_type == 'Duel':
            insert_duel(record, event_id)

        elif event_type == 'Block':
            insert_block(record, event_id)

        elif event_type == 'Clearance':
            insert_clearance(record, event_id)

        elif event_type == 'Interception':
            insert_interception(record, event_id)

        elif event_type == 'Dribble':
            insert_dribble(record, event_id)

        elif event_type == 'Substitution':
            insert_substitution(record, event_id)

        elif event_type == 'Foul Won':
            insert_foul_won(record, event_id)

        elif event_type == 'Foul Committed':
            insert_foul_commit(record, event_id)

        elif event_type == 'Goal Keeper':
            insert_goalie_actions(record, event_id)

        elif event_type == 'Bad Behaviour':
            insert_bad_behaviour(record, event_id)

    elif event_type == 'Pass':
        insert_pass(competition_id, match_id, record)

    elif event_type == 'Shot':
        insert_shot(competition_id, match_id, record)


def insert_play_pattern(play_pattern):
    insert_record('play_patterns', {'play_pattern_id': play_pattern['id'],
                                    'play_pattern_name': play_pattern['name']
                                    })


def insert_related_events(related_events, event_db_id):
    for related_event in related_events:
        insert_record('related_events', {'event_db_id': event_db_id,
                                         'related_event_db_id': related_event
                                         })


def insert_event_outcome(outcome):
    insert_record('event_outcomes', {'event_outcome_id': outcome['id'],
                                     'event_outcome_name': outcome['name']
                                     })


def insert_ball_receipt(record, event_id):
    # if there's no ball_receipt field, there's nothing to add to the ball_receipts table
    br = record.get('ball_receipt')
    if br is None:
        return

    if 'outcome' in record['ball_receipt']:
        outcome = br['outcome']
        outcome_id = outcome['id']
        insert_event_outcome(outcome)

        insert_record('ball_receipts', {'event_id': event_id,
                                        'event_outcome_id': outcome_id
                                        })


def insert_ball_carry(record, event_id):
    # if there's no carry field, there's nothing to add to the ball_carries table
    carry = record.get('carry')
    if carry is None:
        return

    if 'end_location' in carry:
        end_location_x = carry['end_location'][0]
        end_location_y = carry['end_location'][1]
        insert_record('ball_carries', {'event_id': event_id,
                                       'end_location_x': end_location_x,
                                       'end_location_y': end_location_y
                                       })


def insert_pass_height(height):
    insert_record('pass_heights', {'pass_height_id': height['id'],
                                   'pass_height_name': height['name']
                                   })


def insert_body_part(body_part):
    insert_record('body_parts', {'body_part_id': body_part['id'],
                                 'body_part_name': body_part['name']
                                 })


def insert_pass_type(pass_type):
    insert_record('pass_types', {'pass_type_id': pass_type['id'],
                                 'pass_type_name': pass_type['name']
                                 })


def insert_shot_technique(technique):
    insert_record('shot_techniques', {'shot_technique_id': technique['id'],
                                      'shot_technique_name': technique['name']
                                      })


def insert_pass(competition_id, match_id, record):
    event_db_id = record['id']
    related_events = record.get('related_events', [])
    insert_related_events(related_events, event_db_id)

    location_x, location_y = None, None
    if 'location' in record:
        location_x = record['location'][0]
        location_y = record['location'][1]

    duration = record.get('duration', 0)
    under_pressure = record.get('under_pressure')
    counterpress = record.get('counterpress')

    team_id = get_field('teams', 'team_id', {'team_orig_id': record['team']['id'],
                                             'competition_id': competition_id
                                             })
    possession_team_id = get_field('teams', 'team_id', {'team_orig_id': record['possession_team']['id'],
                                                        'competition_id': competition_id
                                                        })

    pass_length = pass_angle = assisted_shot_id = backheel = deflected = None
    miscommunication = is_cross = cut_back = switch = shot_assist = goal_assist = None
    recipient_id = pass_height_id = body_part_id = end_location_x = end_location_y = None
    pass_type_id = event_outcome_id = pass_technique_id = None

    pas = record.get('pass')

    if pas is not None:
        pass_length = pas.get('length')
        pass_angle = pas.get('angle')
        assisted_shot_id = pas.get('assisted_shot_id')
        backheel = pas.get('backheel')
        deflected = pas.get('deflected')
        miscommunication = pas.get('miscommunication')
        is_cross = pas.get('cross')
        cut_back = pas.get('cut_back')
        switch = pas.get('switch')
        shot_assist = pas.get('shot_assist')
        goal_assist = pas.get('goal_assist')

        if 'recipient' in pas:
            recipient_id = pas['recipient']['id']
        if 'height' in pas:
            insert_pass_height(pas['height'])
            pass_height_id = pas['height']['id']
        if 'body_part' in pas:
            insert_body_part(pas['body_part'])
            body_part_id = pas['body_part']['id']
        if 'end_location' in pas:
            end_location_x = pas['end_location'][0]
            end_location_y = pas['end_location'][1]
        if 'type' in pas:
            insert_pass_type(pas['type'])
            pass_type_id = pas['type']['id']
        if 'outcome' in pas:
            insert_event_outcome(pas['outcome'])
            event_outcome_id = pas['outcome']['id']
        if 'technique' in pas:
            insert_shot_technique(pas['technique'])
            pass_technique_id = pas['technique']['id']

    insert_record('events_passes', {'event_db_id': record['id'],
                                    'index': record['index'],
                                    'match_id': match_id,
                                    'team_id': team_id,
                                    'player_id': record['player']['id'],
                                    'period': record['period'],
                                    'minute': record['minute'],
                                    'second': record['second'],
                                    'possession_count': record['possession'],
                                    'possession_team_id': possession_team_id,
                                    'play_pattern_id': record['play_pattern']['id'],
                                    'player_position_id': record['position']['id'],
                                    'location_x': location_x,
                                    'location_y': location_y,
                                    'duration': duration,
                                    'under_pressure': under_pressure,
                                    'counterpress': counterpress,

                                    'recipient_id': recipient_id,
                                    'pass_length': pass_length,
                                    'pass_angle': pass_angle,
                                    'pass_height_id': pass_height_id,
                                    'body_part_id': body_part_id,
                                    'end_location_x': end_location_x,
                                    'end_location_y': end_location_y,
                                    'assisted_shot_id': assisted_shot_id,
                                    'backheel': backheel,
                                    'deflected': deflected,
                                    'miscommunication': miscommunication,
                                    'is_cross': is_cross,
                                    'cut_back': cut_back,
                                    'switch': switch,
                                    'shot_assist': shot_assist,
                                    'goal_assist': goal_assist,
                                    'pass_type_id': pass_type_id,
                                    'event_outcome_id': event_outcome_id,
                                    'pass_technique_id': pass_technique_id
                                    })


def insert_ball_recovery(record, event_id):
    # if there's no ball_recovery field, there's nothing to add to the ball_recoveries table
    br = record.get('ball_recovery')
    if br is None:
        return

    recovery_failure = br.get('recovery_failure')
    offensive = br.get('offensive')

    insert_record('ball_recoveries', {'event_id': event_id,
                                      'recovery_failure': recovery_failure,
                                      'offensive': offensive
                                      })


def insert_duel(record, event_id):
    # if there's no duel field, there's nothing to add to the duels table
    duel = record.get('duel')
    if duel is None:
        return

    duel_type_name = duel_type_id = event_outcome_id = None

    if 'type' in duel:
        duel_type_name = duel['type']['name']
        duel_type_id = duel['type']['id']
    if 'outcome' in duel:
        insert_event_outcome(duel['outcome'])
        event_outcome_id = duel['outcome']['id']

    insert_record('duels', {'event_id': event_id,
                            'duel_type_id': duel_type_id,
                            'duel_type_name': duel_type_name,
                            'event_outcome_id': event_outcome_id
                            })


def insert_block(record, event_id):
    # if there's no block field, there's nothing to add to the blocks table
    block = record.get('block')
    if block is None:
        return

    deflection = block.get('deflection')
    offensive = block.get('offensive')
    save_block = block.get('save_block')

    insert_record('blocks', {'event_id': event_id,
                             'deflection': deflection,
                             'offensive': offensive,
                             'save_block': save_block
                             })


def insert_clearance(record, event_id):
    # if there's no clearance field, there's nothing to add to the clearances table
    clearance = record.get('clearance')
    if clearance is None:
        return

    aerial_won = clearance.get('aerial_won')

    body_part_id = None
    if 'body_part' in clearance:
        insert_body_part(clearance['body_part'])
        body_part_id = clearance['body_part']['id']

    insert_record('clearances', {'event_id': event_id,
                                 'aerial_won': aerial_won,
                                 'body_part_id': body_part_id
                                 })


def insert_interception(record, event_id):
    # if there's no interception field, there's nothing to add to the interceptions table
    interception = record.get('interception')
    if interception is None:
        return

    event_outcome_id = None
    if 'outcome' in interception:
        insert_event_outcome(interception['outcome'])
        event_outcome_id = interception['outcome']['id']

    insert_record('interceptions', {'event_id': event_id,
                                    'event_outcome_id': event_outcome_id
                                    })


def insert_dribble(record, event_id):
    # if there's no dribble field, there's nothing to add to the dribbles table
    dribble = record.get('dribble')
    if dribble is None:
        return

    overrun = dribble.get('overrun')
    nutmeg = dribble.get('nutmeg')
    no_touch = dribble.get('no_touch')

    event_outcome_id = None
    if 'outcome' in dribble:
        insert_event_outcome(dribble['outcome'])
        event_outcome_id = dribble['outcome']['id']

    insert_record('dribbles', {'event_id': event_id,
                               'event_outcome_id': event_outcome_id,
                               'overrun': overrun,
                               'nutmeg': nutmeg,
                               'no_touch': no_touch
                               })


def insert_shot(competition_id, match_id, record):
    event_db_id = record['id']
    related_events = record.get('related_events', [])
    insert_related_events(related_events, event_db_id)

    location_x, location_y = None, None
    if 'location' in record:
        location_x = record['location'][0]
        location_y = record['location'][1]

    duration = record.get('duration', 0)
    under_pressure = record.get('under_pressure')
    counterpress = record.get('counterpress')

    team_id = get_field('teams', 'team_id', {'team_orig_id': record['team']['id'],
                                             'competition_id': competition_id
                                             })
    possession_team_id = get_field('teams', 'team_id', {'team_orig_id': record['possession_team']['id'],
                                                        'competition_id': competition_id
                                                        })

    key_pass_id = aerial_won = follows_dribble = first_time = open_goal = deflected = statsbomb_xg = None
    body_part_id = end_location_x = end_location_y = end_location_z = shot_type_id = event_outcome_id = technique_id = None

    shot = record.get('shot')
    if shot is not None:

        key_pass_id = shot.get('key_pass_id')
        aerial_won = shot.get('aerial_won')
        follows_dribble = shot.get('follows_dribble')
        first_time = shot.get('first_time')
        open_goal = shot.get('open_goal')
        deflected = shot.get('deflected')
        statsbomb_xg = shot.get('statsbomb_xg')

        if 'body_part' in shot:
            insert_body_part(shot['body_part'])
            body_part_id = shot['body_part']['id']
        if 'end_location' in shot:
            end_location_x = shot['end_location'][0]
            end_location_y = shot['end_location'][1]
            if len(shot['end_location']) > 2:
                end_location_z = shot['end_location'][2]
        if 'type' in shot:
            insert_shot_technique(shot['type'])
            shot_type_id = shot['type']['id']
        if 'outcome' in shot:
            insert_event_outcome(shot['outcome'])
            event_outcome_id = shot['outcome']['id']
        if 'technique' in shot:
            insert_shot_technique(shot['technique'])
            technique_id = shot['technique']['id']

    insert_record('events_shots', {'event_db_id': record['id'],
                                   'index': record['index'],
                                   'match_id': match_id,
                                   'team_id': team_id,
                                   'player_id': record['player']['id'],
                                   'period': record['period'],
                                   'minute': record['minute'],
                                   'second': record['second'],
                                   'possession_count': record['possession'],
                                   'possession_team_id': possession_team_id,
                                   'play_pattern_id': record['play_pattern']['id'],
                                   'player_position_id': record['position']['id'],
                                   'location_x': location_x,
                                   'location_y': location_y,
                                   'duration': duration,
                                   'under_pressure': under_pressure,
                                   'counterpress': counterpress,

                                   'key_pass_id': key_pass_id,
                                   'aerial_won': aerial_won,
                                   'follows_dribble': follows_dribble,
                                   'first_time': first_time,
                                   'open_goal': open_goal,
                                   'deflected': deflected,
                                   'statsbomb_xg': statsbomb_xg,
                                   'body_part_id': body_part_id,
                                   'end_location_x': end_location_x,
                                   'end_location_y': end_location_y,
                                   'end_location_z': end_location_z,
                                   'shot_type_id': shot_type_id,
                                   'event_outcome_id': event_outcome_id,
                                   'technique_id': technique_id
                                   })


def insert_substitution(record, event_id):
    # if there's no substitution field, there's nothing to add to the substitutions table
    sub = record.get('substitution')
    if sub is None:
        return

    event_outcome_id = replacement_id = None

    if 'outcome' in sub:
        insert_event_outcome(sub['outcome'])
        event_outcome_id = sub['outcome']['id']
    if 'replacement' in sub:
        replacement_id = sub['replacement']['id']

    insert_record('substitutions', {'event_id': event_id,
                                    'event_outcome_id': event_outcome_id,
                                    'replacement_id': replacement_id
                                    })


def insert_foul_won(record, event_id):
    # if there's no foul_won field, there's nothing to add to the foul_wons table
    foul = record.get('foul_won')
    if foul is None:
        return

    defensive = foul.get('defensive')
    advantage = foul.get('advantage')
    penalty = foul.get('penalty')

    insert_record('foul_wons', {'event_id': event_id,
                                'defensive': defensive,
                                'advantage': advantage,
                                'penalty': penalty
                                })


def insert_foul_type(foul):
    insert_record('foul_types', {'foul_type_id': foul['id'],
                                 'foul_type_name': foul['name']
                                 })


def insert_foul_commit(record, event_id):
    # if there's no foul_committed field, there's nothing to add to the foul_commits table
    foul = record.get('foul_committed')
    if foul is None:
        return

    offensive = foul.get('offensive')
    advantage = foul.get('advantage')
    penalty = foul.get('penalty')

    foul_type_id = card_type = None
    if 'type' in foul:
        insert_foul_type(foul['type'])
        foul_type_id = foul['type']['id']
    if 'card' in foul:
        card_type = foul['card']['name']

    insert_record('foul_commits', {'event_id': event_id,
                                   'foul_type_id': foul_type_id,
                                   'offensive': offensive,
                                   'advantage': advantage,
                                   'penalty': penalty,
                                   'card_type': card_type
                                   })


def insert_goalie_actions(record, event_id):
    # if there's no goalkeeper field, there's nothing to add to the goalkeeper_actions table
    goalie = record.get('goalkeeper')
    if goalie is None:
        return

    gk_position = gk_technique = body_part_id = gk_action_type = event_outcome_id = None

    if 'position' in goalie:
        gk_position = goalie['position']['name']
    if 'technique' in goalie:
        gk_technique = goalie['technique']['name']
    if 'type' in goalie:
        gk_action_type = goalie['type']['name']
    if 'body_part' in goalie:
        insert_body_part(goalie['body_part'])
        body_part_id = goalie['body_part']['id']
    if 'outcome' in goalie:
        insert_event_outcome(goalie['outcome'])
        event_outcome_id = goalie['outcome']['id']

    insert_record('goalkeeper_actions', {'event_id': event_id,
                                         'gk_position': gk_position,
                                         'gk_technique': gk_technique,
                                         'gk_action_type': gk_action_type,
                                         'body_part_id': body_part_id,
                                         'event_outcome_id': event_outcome_id
                                         })


def insert_bad_behaviour(record, event_id):
    # if there's no bad_behaviour field, there's nothing to add to the bad_behaviours table
    bb = record.get('bad_behaviour')
    if bb is None:
        return

    if 'card' in bb:
        card_type = bb['card']['name']
        insert_record('bad_behaviours', {'event_id': event_id,
                                         'card_type': card_type
                                         })
