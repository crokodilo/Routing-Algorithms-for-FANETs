from src.routing_algorithms.BASE_routing import BASE_routing
from src.utilities.utilities import euclidean_distance


class GeoRouting(BASE_routing):

    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)

    def relay_selection(self, opt_neighbors, packet):
        """
        This function returns a relay for packets according to geographic routing.

        @param packet:
        @param opt_neighbors: a list of tuples (hello_packet, drone)
        @return: The best drone to use as relay or None if no relay is selected
        """

        # TODO: Implement your code HERE

        cur_pos = self.drone.coords
        depot_pos = self.drone.depot.coords
        # my_distance_to_depot = util.euclidean_distance(cur_pos, depot_pos)

        best_distance = euclidean_distance(cur_pos, depot_pos)
        best_drone = None
        for hello, neighbor in opt_neighbors:
            neighbor_pos = hello.cur_pos
            neighbor_distance_to_depot = euclidean_distance(neighbor_pos, depot_pos)
            # my_distance_to_neighbor = util.euclidean_distance(cur_pos, neighbor_pos)
            if neighbor_distance_to_depot < best_distance:
                best_drone = neighbor
                best_distance = neighbor_distance_to_depot

        return best_drone
