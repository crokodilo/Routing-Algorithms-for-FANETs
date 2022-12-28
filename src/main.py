import os, sys
sys.path.append(os.getcwd())
from src.simulation.simulator import Simulator
import matplotlib.pyplot as plt
import numpy as np

os.environ["SDL_VIDEODRIVER"] = "dummy"


def main():
    """ the place where to run simulations and experiments. """

    sim = Simulator()   # empty constructor means that all the parameters of the simulation are taken from src.utilities.config.py
    print(f'Running {sim.routing_algorithm.name} routing algorithm.')
    sim.run()            # run the simulation
    
    if sim.routing_algorithm.name == 'QL':
        path = 'data/plots'
        for drone in sim.drones:
            qtable = np.array(drone.routing_algorithm.qtables).T
            plt.figure()
            plt.title(f'q-table for {drone}')
            for d in range(sim.n_drones):
                plt.plot(qtable[d], label=f'q-value for drone {d}')
            plt.legend()
            plt.savefig(f'{path}/{sim.routing_algorithm.name}_qtable_{drone}.png')

        plt.figure()
        for drone in sim.drones:
            plt.title(f'average reward')
            rewards = [r for step, r in drone.routing_algorithm.rewards]
            avg_rewards = [np.mean(rewards[:i]) for i in range(1, len(rewards))]
            
            plt.plot(avg_rewards, label=f'{drone}')
        plt.legend()
        plt.savefig(f'{path}/{sim.routing_algorithm.name}_avg_reward.png')
        
    sim.close()


if __name__ == "__main__":
    main()
