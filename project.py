import sys
import logging

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


class Simulation:
    def __init__(self, config):
        self.config = config
        self.scores = [0 for _ in range(self.config['number_of_player'])]

    def run(self):
        for i in range(self.config['number_of_game']):
            print("Running game #%d" % i)


if __name__ == "__main__":
    sim = Simulation(get_config("config.py"))
    sim.run()
