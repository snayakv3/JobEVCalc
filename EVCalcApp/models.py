from django.db import models

NORMAL = [96, 48, 32, 16, 12, 8, 4]
BOOSTED = [252, 144, 96, 48, 36, 24, 12]
ALL = set(NORMAL + BOOSTED)
SENT_FOR = ['Whole Day', 'Half Day', 'Very Long', 'Long', 'Short', 'Very Short', 'Just A Little']
POWER_ADD_ON = " w/ Power "
POWER_ITEM = {"HP": "Weight", "Atk": "Bracer", "Def": "Belt", "SpA": "Lens", "SpD": "Band", "Spe": "Anklet"}
DAY_STAT_WEIGHT = 3

class EVSpread():
    def __init__(self, ev_data):
        self.hp = ev_data['HP']
        self.atk = ev_data['Atk']
        self.df = ev_data['Def']
        self.spatk = ev_data['SpA']
        self.spdf = ev_data['SpD']
        self.spe = ev_data['Spe']
        self.ev_calc_splits = {
            stat: (ev_data[stat], EVSpread.calc_best_ev(ev_data[stat])) for stat in ev_data
        }

    @staticmethod
    def calc_best_ev(number):
       best_calc = []
       possibilties = [x for x in ALL if x <= number and x > number//2]
       for possibility in possibilties:
          current_calc = []
          if possibility == number:
              return [possibility]
          else:
              current_calc = [possibility] + EVSpread.calc_best_ev(number-possibility)
          if sum(current_calc) == number and (len(best_calc) == 0 or len(best_calc) >= len(current_calc)):
                  best_calc = current_calc
       return best_calc

    def is_zero(self):
        total_ev = self.hp + self.atk + self.df + self.spatk + self.spdf + self.spe
        return total_ev == 0

    def __str__(self):
        to_string = f"\tHP: {self.hp} \n\tAtk: {self.atk}\n\tDef: {self.df}"
        to_string += f"\n\tSpA: {self.spatk}\n\tSpD: {self.spdf}\n\tSpe: {self.spe}\n"
        return to_string


class Pokemon:
    used_names = {}
    def __init__(self, name, ev_spread):
        if not name in Pokemon.used_names:
            Pokemon.used_names[name] = 1
            self.name = name
            self.id = 1
        else:
            Pokemon.used_names[name] += 1
            self.name = name
            self.id = Pokemon.used_names[name]
        self.ev_spread = ev_spread

    def subtract_evs(self, stat, amount):
        if stat == 'HP':
            self.ev_spread.hp -= amount
        elif stat == 'Atk':
            self.ev_spread.atk -= amount
        elif stat == 'Def':
            self.ev_spread.df -= amount
        elif stat == 'SpA':
            self.ev_spread.spatk -= amount
        elif stat == 'SpD':
            self.ev_spread.spdf -= amount
        elif stat == 'Spe':
            self.ev_spread.spe -= amount

    def has_no_evs(self):
        return self.ev_spread.is_zero()

    def ev_calc_copy(ev_calc):
        copy = {}
        for ev in calc:
            copy[ev] = calc[ev]
        return copy

    def get_ev_calcs(self):
        return self.ev_spread.ev_calc_splits
    def get_unique_name(self):
        unique_name = self.name
        if Pokemon.used_names[unique_name] > 1:
            unique_name += f" ({self.id})"
        return unique_name
    def __str__(self):
        return "{}\n{}".format(self.name.upper(), self.ev_spread)

class Day:
    num = 0
    def __init__(self):
        self.jobs = {}
        Day.num += 1
        self.num = Day.num

    def get_jobs(self):
        return self.jobs

    def get_num(self):
        return self.num

    def get_total_pokemon(self):
        total = 0
        for stat in self.jobs:
            total += DAY_STAT_WEIGHT
            total += len(self.jobs[stat][1])
        return total

    def get_stats_job_length(self):
        list = []
        for stat in self.jobs:
            amount = self.jobs[stat][0]
            pokemon = self.jobs[stat][1]
            time = None
            if POWER_ADD_ON in pokemon:
                time = SENT_FOR[BOOSTED.index(amount*3)]
            else:
                time = SENT_FOR[NORMAL.index(amount)]
            list.append([stat, time, pokemon, amount])
        return list
