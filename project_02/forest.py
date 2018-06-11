
class Tree:
    def __init__(self, root_label='root', value=None):
        """A basic non binary tree class. It creates a root node that may
        have other trees as children."""
        self.root = Node(label=root_label, value=value)
        self.tree_map = {}

    def build_map(self, max_depth=None):
        """Builds the tree map"""
        self.tree_map[self.root.label] = self.root.get_sub_tree(max_depth)

    def calculate_mmv(self, minmax=1, update=True):
        """Min max calculation using same function from Node.

        :param minmax: Determines if next level should be searched for max or min. Set to 1 for max and to -1 for min.
        :param update: Flag if a given node value should be updated by looking on its childrens values.

        :returns: Value of this tree.
        """
        return self.root.calculate_mmv(minmax=minmax, update=update)


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

    def add_child(self, label='Node', value=None):
        """Adds a child node to the tree.

        :param nid: Node ID
        :param label: Label for the tree root to use
        :param value: Some value the node holds
        """
        nid = self.nid + len(self.children)
        self.children.append(Node(nid, label, value))

    def get_sub_tree(self, max_depth=None):
        """Gives a subtree of this node as dict.

        :param max_depth: States how deep the algorithm should look.

        :returns: SubTree dict.
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

    def calculate_mmv(self, minmax=1, update=True):
        """Determines the MinMaxValue for this node.

        :param minmax: Determines if next level should be searched for max or min. Set to 1 for max and to -1 for min.
        :param update: Flag if a given node value should be updated by looking on its childrens values.

        :returns: Value of this node.
        """

        # Dictionary that maps min or max function
        mmd = {
            1: max,
            -1: min
        }

        # Value of this node
        value = self.value
        child = self.label

        if update or self.value is None:
            # Loop over the list of children not had_no_value and update and
            if len(self.children) > 0:

                # Value list for children
                vl = []
                for child in self.children:
                    vl.append(child.calculate_mmv(minmax=minmax * -1, update=update)[0])

                # Take the Min / Max value (depends on level of tree)
                value = mmd[minmax](vl)
                child = self.children[vl.index(value)].label
                self.value = value

        return value, child

    def __str__(self):
        """Overwriting to string"""
        return "('{}'-> {})".format(self.label, self.value)
