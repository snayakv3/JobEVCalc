from django.shortcuts import render
from . import ev_parser as parse, ev_setup as setup, ev_calc as calc
import logging, time

NOT_DONE = "has not been done"
NUM_OF_CHECKS = 4
view_logger = logging.getLogger('main_logger')
logging.Formatter.converter = time.gmtime
formatter = logging.Formatter(fmt="%(levelname)s(%(thread)d): %(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler = logging.FileHandler('./EVCalcApp/logs/application.log')
file_handler.setFormatter(formatter)
view_logger.addHandler(file_handler)
view_logger.setLevel(logging.INFO)

def index(request):
    if(request.POST):
        parse_check, setup_check, number_of_days_check, evs_fulfilled_check = (NOT_DONE for _ in range(0, NUM_OF_CHECKS))
        context={
            'error':'Could not complete the calculation, please try again later'
        }

        team_data = request.POST.get('team')
        pokemon_team, error, parse_check = parse.team_parser(team_data)
        if parse_check:
            stat_map = setup.set_common_stats(pokemon_team)
            setup_check = setup.check_common_team(pokemon_team, stat_map)

            if setup_check:
                best_days = calc.optimal_calc(pokemon_team, stat_map)
                number_of_days_check = calc.check_days_number(pokemon_team, best_days)
                power_items, evs_fulfilled_check = calc.get_power_items_and_check(pokemon_team, best_days)
                if number_of_days_check and number_of_days_check:
                    context={
                        'days' : best_days,
                        'power_items':power_items,
                        'user_input':team_data,
                        'error':error
                    }
                    view_logger.info("days have been calculated, now sending to display")
        else:
            context['error'] = error

        if not setup_check or not number_of_days_check or not number_of_days_check:
            view_logger.error("stat EV splits in stat mapping setup accounted for: {}".format(setup_check))
            view_logger.error("amount of pokemon in all days account for amount of pokemon needs in stat mapping: {}".format(number_of_days_check))
            view_logger.error("total EV's for each pokemon in all days account for their EV needs: {}".format(evs_fulfilled_check))


        return render(request, 'EVCalc_app/index.html', context=context)

    else:
        return render(request, 'EVCalc_app/index.html')

def error(request):
    return render(request, 'EVCalc_app/error.html')
