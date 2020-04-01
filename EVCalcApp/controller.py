from . import ev_parser as parse, ev_setup as setup, ev_calc as calc, ev_error as error

def get_client_ip(meta_data):
   x_forwarded_for = meta_data.get('HTTP_X_FORWARDED_FOR')
   if x_forwarded_for:
       ip = x_forwarded_for.split(',')[0]
   else:
       ip = meta_data.get('REMOTE_ADDR')
   return ip

def calculate_job_ev_days(team_data, meta_data):
    setup_check, number_of_days_check, evs_fulfilled_check = (error.NOT_DONE for _ in range(0, error.NUM_OF_CHECKS))
    error_message = error.DEFAULT_MESSAGE
    best_days = None
    power_items = None
    return_team_data = None

    try:
        pokemon_team, error_message, parse_check = parse.team_parser(team_data)
        if parse_check:
            stat_map = setup.set_common_stats(pokemon_team)
            setup_check = setup.check_common_team(pokemon_team, stat_map)
            if setup_check:
                possible_best_days = calc.optimal_calc(pokemon_team, stat_map)
                number_of_days_check = calc.check_days_number(pokemon_team, possible_best_days)
                possible_power_items, evs_fulfilled_check = calc.get_power_items_and_check(pokemon_team, possible_best_days)
                if number_of_days_check and number_of_days_check:
                    best_days = possible_best_days
                    power_items = possible_power_items
                    return_team_data = team_data
        else:
            return_team_data = team_data
    except Exception as err:
        exception_message = "Found exception: {}".format(err)
        error.write_logs(get_client_ip(meta_data), team_data, exception_message)
        error_message = error.DEFAULT_MESSAGE
    else:
        if parse_check and best_days is None:
            error.create_logs(get_client_ip(meta_data), team_data, setup_check, number_of_days_check, evs_fulfilled_check)
            error_message = error.DEFAULT_MESSAGE

    return error_message, best_days, power_items, return_team_data
