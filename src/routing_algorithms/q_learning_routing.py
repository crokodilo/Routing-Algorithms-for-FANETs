from src.routing_algorithms.BASE_routing import BASE_routing
from src.utilities import utilities as util
import numpy as np

class QLearningRouting(BASE_routing):

    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone=drone, simulator=simulator)
        self.taken_actions = {}  # id event : (old_state, old_action)
        self.random = np.random.RandomState(self.simulator.seed)
        
        self.q_table = [0]*self.simulator.n_drones # Q-table for the two actions: keep or pass the packet.
        self.n_updates = [0]*self.simulator.n_drones
        
        self.epsilon = 0.01
        self.qtables = []
        self.rewards = []

    def _linear_reward(self, delay, outcome):
        
        if outcome == -1:
            return -10
        
        max_delay = self.simulator.event_duration

        return 5*(1 - delay / max_delay)


    def _hyperbolic_reward(self, delay, outcome):
        if outcome == -1:
            return -1

        return 1 / (delay + 1)

    def best_action_q_table(self, neighbors_plus_me):
        
        mask = np.ones(self.simulator.n_drones, dtype = bool)
        mask[neighbors_plus_me] = False
        
        possible_actions = np.ma.array(self.q_table, mask=mask)
        
        random_tie_breaking = np.flatnonzero(possible_actions == possible_actions.max())
        
        return self.random.choice(random_tie_breaking)



    def feedback(self, drone, id_event, delay, outcome):
        """
        Feedback returned when the packet arrives at the depot or
        Expire. This function have to be implemented in RL-based protocols ONLY
        @param drone: The drone that holds the packet
        @param id_event: The Event id
        @param delay: packet delay
        @param outcome: -1 or 1 (read below)
        @return:
        """

        # outcome can be:
        #   -1 if the packet/event expired;
        #   1 if the packets has been delivered to the depot

        # Be aware, due to network errors we can give the same event to multiple drones and receive multiple
        # feedback for the same packet!!

        if id_event in self.taken_actions:
            
            action = self.taken_actions[id_event]
            
            self.n_updates[action] += 1

            reward = self._linear_reward(delay, outcome)
            # remove the entry, the action has received the feedback
            del self.taken_actions[id_event]

            # reward or update using the old state and the selected action at that time
            # do something or train the model
            self.rewards.append((self.simulator.cur_step, reward))
            self.q_table[action] += (reward - self.q_table[action]) / self.n_updates[action]

            self.qtables.append(self.q_table.copy())

    def relay_selection(self, opt_neighbors: list, packet):
        """
        This function returns the best relay to send packets.
        @param packet:
        @param opt_neighbors: a list of tuple (hello_packet, source_drone)
        @return: The best drone to use as relay
        """
        # TODO: Implement your code HERE
    
        hello_packets = [pack for pack, _ in opt_neighbors]
        neighbors = [drone for _, drone in opt_neighbors]

        neighbors_plus_me = neighbors + [self.drone]

        neighbors_plus_me_ids = [d.identifier for d in neighbors_plus_me]
        
        if self.random.rand() < self.epsilon:
            action = self.random.choice(neighbors_plus_me_ids)
        else:
            action = self.best_action_q_table(neighbors_plus_me_ids)
        
        # Store your current action --- you can add some stuff if needed to take a reward later
        self.taken_actions[packet.event_ref.identifier] = (action)

        for drone in neighbors_plus_me:
            if drone.identifier == action:
                return drone