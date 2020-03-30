from .models import Day, NORMAL, BOOSTED, POWER_ITEM, POWER_ADD_ON


def get_only_unique_and_same(pokemons):
    #!!!!!! This is partially bad cause I'm splitting up unique in to pieces of
    #!!!!!! 10 but same is getting checking for all of them when it shouldn't
    #!!!!!! would need to reevaluate the module as a whole so I will defer it
    checked = []
    unique = [[],]
    same = [[],]
    same_checks = [[],]
    unique_index = 0
    for pokemon in pokemons:
        only_pokemon_name = pokemon.rsplit(POWER_ADD_ON)[0]
        if only_pokemon_name not in checked:
            checked.append(only_pokemon_name)
            if len(unique[unique_index]) == 10:
               unique_index += 1
               unique.append([])
            unique[unique_index].append(pokemon)
        else:
            added = False
            for i in range(0, len(same_checks)):
                if only_pokemon_name not in same_checks[i]:
                    same_checks[i].append(only_pokemon_name)
                    same[i].append(pokemon)
                    added = True
                    break
            if not added:
                same_checks.append([only_pokemon_name])
                same.append([pokemon])

    return unique + same

def get_ordered_common_stat_ev(stat, stat_map):
    if stat_map is None or stat not in stat_map:
        return None
    else:
        stat_evs = stat_map[stat]
        max_ev = []
        stat_ev_list = list(stat_evs.keys())
        while len(stat_ev_list) > 0:
            next_ev = None
            next_ev_num = 0
            for j in range(0, len(stat_ev_list)):
                ev = stat_ev_list[j]
                ev_num = len(get_only_unique_and_same(stat_evs[ev])[0])
                if next_ev is None:
                    next_ev = ev
                    next_ev_num = ev_num
                elif ev_num > next_ev_num:
                    next_ev = ev
            max_ev.append(next_ev)
            stat_ev_list.remove(next_ev)
        return max_ev

def return_best_stat_ev(stat, ordered_evs, used, team, stat_map):
    target_stat = stat_map[stat]
    max_available_team = None
    max_available_ev = None
    for ev in ordered_evs:
        job_teams = get_only_unique_and_same(target_stat[ev])
        for job_team in job_teams:
            valid_job_team = True
            for pokemon in job_team:
                valid_job_team = valid_job_team and pokemon.rsplit(POWER_ADD_ON)[0] not in used
            if len(job_team) > 0 and valid_job_team and (max_available_ev is None or len(job_team) > len(max_available_team)):
                max_available_team = job_team
                max_available_ev = ev

    if max_available_ev is not None:
        target_team = target_stat[max_available_ev]
        is_done = len(max_available_team) == len(target_team)
        for pokemon in max_available_team:
            used.append(pokemon.rsplit(POWER_ADD_ON)[0])
            if not is_done:
                target_team.remove(pokemon)
        if is_done:
            del target_stat[max_available_ev]

    return max_available_ev, max_available_team


def optimal_calc(team, stat_map):
    best_days = []
    needed_stats = [stat for stat in stat_map if len(stat_map[stat]) > 0]
    team_names = [pokemon.get_unique_name() for pokemon in team]

    while(len(needed_stats) > 0):
        day = Day()
        enlisted = []
        stat_index = 0
        while stat_index < len(needed_stats) and len(enlisted) < len(team):
            stat = needed_stats[stat_index]
            target_stat = stat_map[stat]
            ordered_ev_stats = get_ordered_common_stat_ev(stat, stat_map)
            ev, pokemon_needed = return_best_stat_ev(stat, ordered_ev_stats, enlisted, team, stat_map)
            if ev is not None:
                day.jobs[stat] = (ev, pokemon_needed)
            stat_index += 1

        best_days.append(day)
        needed_stats = [stat for stat in stat_map if len(stat_map[stat]) > 0]

    # Reorder days based on length for calendar
    best_days.sort(key=lambda day : day.get_total_pokemon(), reverse=True)
    for i in range(0,len(best_days)):
        day = best_days[i]
        day.num = i+1
        # print("Day",day.get_num(), day.get_total_pokemon())
        # for stat in day.get_jobs():
        #     print("\t",stat, day.get_jobs()[stat])
    Day.num = 0
    return best_days

#Test
def check_days_number(team, days):
    expected_count = 0
    for pokemon in team:
        ev_calc = pokemon.get_ev_calcs()
        for stat in ev_calc:
            expected_count += len(ev_calc[stat][1])

    actual_count = 0
    for day in days:
        for stat in day.get_jobs():
            actual_count += len(day.get_jobs()[stat][1])
    return actual_count == expected_count

#Test
def get_power_items_and_check(team, days):
    name_pokemon = {pokemon.get_unique_name() : pokemon for pokemon in team}
    stat_max_power_item = { 'HP':0, 'Atk':0, 'Def':0, 'SpA':0, 'SpD':0, 'Spe':0 }
    for day in days:
        for stat in day.get_jobs():
            amount, pokemons = day.get_jobs()[stat]
            current_power_item = 0
            for pokemon in pokemons:
                indiv_amount = amount
                if POWER_ADD_ON in pokemon:
                    indiv_amount = BOOSTED[NORMAL.index(amount)]
                    current_power_item += 1
                pokemon_name = pokemon.rsplit(POWER_ADD_ON)[0]
                actual_pokemon = name_pokemon[pokemon_name]
                actual_pokemon.subtract_evs(stat, indiv_amount)
            if stat_max_power_item[stat] < current_power_item:
                stat_max_power_item[stat] = current_power_item
    all_zero = True
    for pokemon in team:
        all_zero = all_zero and pokemon.has_no_evs()

    actual_power_items = [[POWER_ITEM[stat], stat_max_power_item[stat]] for stat in POWER_ITEM]

    return actual_power_items, all_zero
