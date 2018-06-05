
class Tree:
    def __init__(self, label='root', value=None):
        """A basic non binary tree class. It creates a root node that may
        have other trees as children."""
        self.root = Node(label=label, value=value)
        self.tree_map = {}

    def build_map(self, max_depth=None):
        """Builds the tree map"""
        self.tree_map[self.root.label] = self.root.get_sub_tree(max_depth)


class Node:
    def __init__(self, nid=0, label='root', value=None):
        """Node class that can have multiple children.

        :param nid: Node ID
        :param label: Label for the tree root to use
        :param value: Some value the node holds
        """
        self.nid = nid

        # List of subtrees
        self.children = []

        # Label and value for THIS node
        self.label = label
        self.value = value

    def calculate_MMV(self):
        """Calculates the min-max value from the point of view of this node."""
        pass

    def add_child(self, label='Node', value=None):
        """Adds a child node to the tree.

        :param nid: Node ID
        :param label: Label for the tree root to use
        :param value: Some value the node holds
        """
        nid = self.nid + len(self.children)
        self.children.append(Node(nid, label, value))

    def get_sub_tree(self, max_depth=None):
        """Gives the subtree information for this node.

        :param max_depth: States how deep the algorithm should look.
        """
        sub_tree = {'v': self.value}
        if len(self.children) > 0:
            sub_tree['c'] = {}
            if max_depth is None:
                for child in self.children:
                    sub_tree['c'][child.label] = child.get_sub_tree()

            else:
                new_max_depth = max_depth - 1
                if new_max_depth > 0:
                    for child in self.children:
                        sub_tree['c'][child.label] = child.get_sub_tree()

        return sub_tree

    def __str__(self):
        """Overwriting to string"""
        return "('{}'-> {})".format(self.label, self.value)
