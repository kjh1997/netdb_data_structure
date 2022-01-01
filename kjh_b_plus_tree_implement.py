class node:
    '''
    pkey = parent key
    ckey = child key
    isleaf = this is leaf node?
    values = if this node isn't leaf node, then this node don't have values
    root = root node
    keys = keys to this node.
    '''
    def __init__(self, root):
        self.root = root
        self.pkey = None
        self.ckey = None
        self.isleaf = False
        self.values = []
        self.keys = []

class b_plus_tree_config:
    '''
    this class need to config tree.
    init root node
    '''
    def __init__(self, root, degree):
        self.degree = degree
        self.root = node(root)

    def insert_value(self, value, key):
        