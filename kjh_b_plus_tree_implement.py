import math
import time
class node:
    '''
    pkey = parent key
    ckey = child key
    isleaf = this is leaf node?
    values = if this node isn't leaf node, then this node don't have values
    root = root node
    keys = keys to this node.
    '''
    def __init__(self, t_f):
      #  self.root = t_f # 맨 꼭대기 노드?
        self.pkey = None # 부모 키
                         # 자식노드가 부모노드와 상호작용하기위해 사용함.
        
        self.ckey = None # 아이 키 >> 리프노드는 연결리스트 구조.
                         # leaf node에서의 연결리스트를 구현하기 위해 존재함.
        self.isleaf = t_f # 리프노드 ?
        self.values = [] # 값
        self.keys = [] # 값에 대한 키

    def insert(self, leaf, value, key):
        if (self.values):
            temp = self.values
            for i in range(len(temp)):
                if value < temp[i]:
                    '''
                    넣으려는 값이 leaf_node의 i번째 값 보다 작을 때.

                    '''
                    self.values = self.values[:i] + [value]  + self.values[i:]
                    self.keys = self.keys[:i] + [key]  + self.keys[i:]
                elif i+1 == len(temp):
                    '''
                    i+1이 values의 길이랑 같으면 끝에다 넣음.
                    '''
                    self.values.append(value)
                    self.keys.append(key)
        else:
            self.values = [value]
            self.keys = [key]
        print(self, self.keys)

class b_plus_tree_config:
    '''
    this class need to config tree.
    init root node
    '''
    def __init__(self, degree):
        '''
        b_plus_tree configuration
        '''
        self.degree = degree
        self.root_node = node(True)
# ----------------------------------삽입 기능 ---------------------------------- 
    def insert_value(self, value, key):
        '''
        key, value 삽입 과정
        '''
        leaf_node = self.find_leaf_node(value)
        leaf_node.insert(leaf_node, key, value)
        if(len(leaf_node.values) == self.degree):
            # leaf_node에 값을 넣었는데, 이 values의 길이가 degree랑 같으면 decompose가 일어나야함.
            add_leaf_node = node(True)
            add_leaf_node.pkey = leaf_node.pkey
            mid_key = int(math.ceil(self.degree /2)) - 1
            add_leaf_node.values = leaf_node.values[mid_key+1:]
            add_leaf_node.keys = leaf_node.keys[mid_key+1:]
            leaf_node.keys = leaf_node.keys[:mid_key+1]
            leaf_node.values = leaf_node.values[:mid_key+1]
            print('1',leaf_node.values)
            print('2',add_leaf_node.values)
            leaf_node.ckey = add_leaf_node
            self.new_internal_node(leaf_node, add_leaf_node.values[0], add_leaf_node)

    def new_internal_node(self, prior_node, std_value, new_node):
        # 노드가 나눠짐에 따라 새로운 internal node를 만들어야한다. 이 노드는 leafnode가 아니다.
        if (self.root_node == prior_node):
            # 초기에 root node가 leaf node이면 이거만 수행하면 됨.
            root_node = node(False)
            root_node.values = [std_value]
            root_node.keys = [prior_node, new_node]
            self.root_node = root_node
            prior_node.pkey = new_node
            new_node.pkey = new_node
            return

        pnode = prior_node.pkey
        temp = pnode.keys
        for i in range(len(temp)):
            # 부모 노드의 키
            if (temp[i] == prior_node):
                pnode.keys = pnode.keys[:i + 1] + [new_node] + pnode.keys[i+1:]
                pnode.values = pnode.values[:i + 1] + [std_value] + pnode.values[i+1:]
                if (len(pnode.values) == self.degree):
                    # 부모 노드의 len(값) == degree 일 경우 decompose가 일어남.
                    add_pnode = node(False)
                    add_pnode.pkey = pnode.pkey
                    mid_key = math.ceil(self.degree/2) -1
                    add_pnode.values = pnode.values[mid_key+1:]
                    add_pnode.keys = pnode.keys[mid_key+1:]
                    pnode.values = pnode.values[:mid_key+1]
                    pnode.keys = pnode.keys[:mid_key+1]
                    self.new_internal_node(pnode, add_pnode.values[0], add_pnode)

    def find_leaf_node(self, value):        
        current_node = self.root_node
        while(current_node.isleaf == False):
            '''
            leaf node에 넣어야하므로 leaf node를 찾는다.
            '''
            temp = current_node.values
            for i in range(len(temp)):
                
                if (value == temp[i]):
                    '''
                    넣으려는 값이 현재 노드의 i번째 값이랑 같을 때
                    '''
                    current_node = current_node.keys[i + 1]
                    break
                elif (value < temp[i]):
                    '''
                    넣으려는 값이 현재 노드의 i번째 값보다 작을 때
                    '''
                    current_node = current_node.keys[i]
                    break
                elif (i + 1 == len(current_node.values)):
                    '''
                    넣으려는 값이 현재 노드의 길이와 같을 때
                    value의 길이가 1이면 key값의 범위는 0,1이다.
                    그러므로 i+1이 현재 값의 길이와 같으면 마지막 key를 선택한다.
                    '''
                    current_node = current_node.keys[i+1]
                    break
        return current_node

    
# ---------------------------------------- 삽입 기능 끝 ------------------------------------- 

        

btree_degree = 3
bptree = b_plus_tree_config(btree_degree)
bptree.insert_value(5,33)
bptree.insert_value(7,34)
bptree.insert_value(73,34)
bptree.insert_value(71,3432)
bptree.insert_value(3,3177)
bptree.insert_value(6,3727)
bptree.insert_value(21,37407)
bptree.insert_value(32,31777)
bptree.insert_value(66,37257)
bptree.insert_value(281,37247)
