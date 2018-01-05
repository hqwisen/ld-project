import sys
import logging
from random import uniform

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_config(configfile):
    try:
        config = {}
        exec(open(configfile).read(), config)
        del config['__builtins__']
        return config
    except FileNotFoundError:
        print("Error: '%s' file not found." % configfile)
        sys.exit(1)
    except Exception as e:
        log.error("Config Error: %s", e)
        sys.exit(1)

class Player:
    def __init__(self, player_id, intuitive, p, b, c, delibaration_plays):
        self.id = player_id
        self.intuitive = intuitive
        self.p = p
        self.b = b
        self.c = c
        self.delibaration_plays = delibaration_plays
        self.threshold = 0
        self.game_information = -1
        self.compute_threshold()

    def compute_threshold(self):
        if self.intuitive == 0 and self.p >= (self.c / self.b): # If inuitively cooperator & condition is met
            self.threshold = self.c * (1 - self.p)

    def pay_to_find_out(self, cost):
        return cost <= self.threshold

    def update_game_information(self, game):
        self.game_information = game

    def get_action(self):
        if self.game_information != -1:
            game_info = self.game_information
            self.game_information = -1
            return self.delibaration_plays[game_info]
        return self.intuitive

class Simulation:
    def __init__(self, config):
        self.config = config
        self.scores = [0 for _ in range(self.config['number_of_players'])]
        self.players = []
        self.generate_players()

    def generate_players(self):
        for player_id in range(self.config['number_of_players']):
            self.players.append(Player(player_id,
                                        self.config['player{0}_int'.format(player_id+1)],
                                        self.config['p'],
                                        self.config['b'],
                                        self.config['c'],
                                        self.config['delibaration_plays']))

    def generate_game(self, p):
        if p <= uniform(0, 1):
            return (1, self.config['gamma1'])
        return (0, self.config['gamma0'])

    def generate_cost(self):
        return uniform(*self.config['cost_dist'])

    def compute_rewards(self, rewards, id1, action1, id2, action2):
        self.scores[id1] += rewards[action1][action2]
        self.scores[id2] += rewards[action2][action1]

    def get_average_scores(self):
        return list(map(lambda x: x / self.config['number_of_games'], self.scores))

    def run(self):
        for i in range(self.config['number_of_games']):
            #print("Running game #%d" % i)
            game_id, rewards = self.generate_game(self.config['p'])
            cost = self.generate_cost()
            players_actions = []
            for player in self.players:
                if player.pay_to_find_out(cost):
                    player.update_game_information(game_id)
                    self.scores[player.id] -= cost
                players_actions.append(player.get_action())
            for i in range(0, len(players_actions), 2):
                self.compute_rewards(rewards, i, players_actions[i], i+1, players_actions[i+1])
        print(self.get_average_scores())

if __name__ == "__main__":
    sim = Simulation(get_config("config.py"))
    sim.run()
