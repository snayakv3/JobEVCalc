import re
from .models import Pokemon, EVSpread

def name_parser(data):
    """
    Parse the name line of pokemon's data and return the name

    :param data: str containing raw name data
    :returns: str containing Pokemon name
    """
    # used regex with negative lookbehind and positive lookahead
    name_data = re.split("(?<!\.) (?=\(|\@)", data.strip())
    name = name_data[0]
    #matching if next element has (CC) where C is any number or char
    if len(name_data) > 1 and re.match("^\(..+\)$", name_data[1]) is not None:
        name = name_data[1].replace("(","").replace(")","")
    return name

def ev_parser(data):
    """
    Parse raw line of EV data of a pokemon's data and return an EVSpread object with respective
    information

    :param data: str containing raw EV data
    :returns: EVSpread object
    """
    data = data.strip()
    ev_spread_data = { 'HP':0, 'Atk':0, 'Def':0, 'SpA':0, 'SpD':0, 'Spe':0 }
    stat_ev_raw_data = data.split(' / ')
    for stat_ev in stat_ev_raw_data:
        ev, stat = stat_ev.strip().split(' ')
        if stat not in ev_spread_data or not ev.isdigit() or int(ev) > 252:
            return None
        ev_spread_data[stat] = int(ev)
    return EVSpread(ev_spread_data)

def team_parser(data):
    """
    Parse raw team data and return a team of Pokemon with name and EVSpread set along with an
    error string if any has occurred

    :param data: str containing raw pokemon team data delimited with proper white space
    :returns: list of Pokemon objects with str for error message
    """
    Pokemon.used_names={}
    data = data.replace('\r','')
    pokemon_data = data.strip("\n").split("\n\n")
    team=[]
    errors = None
    no_ev_pokemon = []

    for data in pokemon_data:
        data = data.split('\n')
        name = name_parser(data.pop(0))
        ev_spread = None
        for line in data:
            if "EVs:" in line:
                ev_data = line[4:]
                # not enough to catch everything but should work for the time being
                if re.fullmatch("^[0-9HPAtkDefSp\/' ']+$", ev_data):
                    ev_spread = ev_parser(ev_data)
        if ev_spread is None:
           no_ev_pokemon.append(name)
        else:
            pokemon = Pokemon(name=name, ev_spread=ev_spread)
            team.append(pokemon)

    if len(team) == 0:
        errors="Invalid team data, please read the FAQ for help"
    elif not len(no_ev_pokemon) == 0:
        errors = "Problems reading EVs for some pokemon: "
        for i in range(0, len(no_ev_pokemon)-1):
            errors += "{}, ".format(no_ev_pokemon[i])
        errors += no_ev_pokemon[-1]
    return team, errors, not len(team) == 0
