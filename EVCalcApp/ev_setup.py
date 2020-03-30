from .models import NORMAL, BOOSTED, POWER_ADD_ON, POWER_ITEM

def get_normal_ev(power_ev):
    if power_ev in BOOSTED:
        time_index = BOOSTED.index(power_ev)
        return NORMAL[time_index]
    else:
        return -1

def pokemon_in_list_already(item, ev_list):
    for pokemon in ev_list:
        if item == pokemon.rsplit(POWER_ADD_ON)[0]:
            return True
    return False

def add_deferred(stat, ev_pokemon, stat_map):
    target = stat_map[stat]
    for ev in ev_pokemon:
        normal_ev = get_normal_ev(ev)
        for pokemon in ev_pokemon[ev]:
            #this needs to be reevaluated....
            if ev in target and (not pokemon_in_list_already(pokemon, target[ev]) or normal_ev not in target):
                    target[ev] += [pokemon.get_unique_name()]
            elif normal_ev in target:
                target[normal_ev] += [pokemon.get_unique_name() + POWER_ADD_ON + POWER_ITEM[stat]]
            else:
                target[ev] = [pokemon.get_unique_name()]

def add_pokemon_to_common_stats(stat_evs, ev_calc, stat, pokemon, deferred):
    ev_job_layout = ev_calc[stat][1]
    for ev in ev_job_layout:
        if ev in NORMAL and ev in BOOSTED:
            if ev in deferred:
               deferred[ev].append(pokemon)
            else:
               deferred[ev] = [pokemon]
        else:
            normal_ev = get_normal_ev(ev)
            pokemon_to_append = pokemon.get_unique_name()
            if normal_ev != -1:
                ev = normal_ev
                pokemon_to_append += POWER_ADD_ON + POWER_ITEM[stat]
            if ev in stat_evs:
                stat_evs[ev].append(pokemon_to_append)
            else:
                stat_evs[ev] = [pokemon_to_append]

def set_common_stats(team):
    stat_map = {'HP':{}, 'Atk':{}, 'Def':{}, 'SpA':{}, 'SpD':{}, 'Spe':{}}

    for stat in ['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe']:
        stat_evs = stat_map[stat]
        deferred = {}
        for pokemon in team:
            ev_calc = pokemon.get_ev_calcs()
            if stat in ev_calc:
                ev_job_layout = ev_calc[stat][1]
                add_pokemon_to_common_stats(stat_evs, ev_calc, stat, pokemon, deferred)
        add_deferred(stat, deferred, stat_map)
    return stat_map

#Test
def check_common_team(team, stat_map):
    expected_count = 0
    for pokemon in team:
        for stat in pokemon.get_ev_calcs():
            expected_count += len(pokemon.get_ev_calcs()[stat][1])
    actual_count = 0
    for stat in stat_map:
         for ev in stat_map[stat]:
             actual_count += len(stat_map[stat][ev])
    return actual_count == expected_count
