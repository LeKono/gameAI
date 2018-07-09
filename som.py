import numpy as np
import networkx as nx


class SOM:
    def __init__(self, number_of_nodes=10, dataset=None):
        """A basic SOM implementation.

        :param number_of_nodes: Number of nodes in the resulting SOM graph.
        :param dataset: A n-dimensional dataset that the SOM should be computed for.
        """

        # Creates a random dataset containing colorcoding if no dataset is passed
        self.dataset = dataset if dataset is not None else np.random.randint(0, 255, (3, 100))
        self.graph = self.train(number_of_nodes, dataset)

    def train(self, number_of_nodes, dataset, circular=True, update=False):
        """This method trains the SOM graph on the dataset given.

        :param number_of_nodes: Number of nodes in the resulting SOM graph.
        :param dataset: A n-dimensional dataset that the SOM should be computed for.
        :param circular: States if the resulting SOM graph should be circular.
        :param update: Flag that states if a new graph should be created or the existing graph in this object should
        be updated.

        :returns: NetworkX Graph
        """
        tmp_graph = nx.Graph()

        for i in range(number_of_nodes):
            node_name = "n{}".format(i)
            tmp_graph.add_node(node_name)

            if "n{}".format(i-1) in tmp_graph.nodes:
                tmp_graph.add_edge("n{}".format(i-1), node_name, w="WEIGHT()")

        if circular:
            tmp_graph.add_edge("n{}".format(number_of_nodes - 1), "n0")

        if update:
            self.graph = tmp_graph

        return tmp_graph
