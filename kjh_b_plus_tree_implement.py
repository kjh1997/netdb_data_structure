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
        self.pkey = None # 부모 키
                         # 자식노드가 부모노드와 상호작용하기위해 사용함.
        
        self.ckey = None # 아이 키 >> 리프노드는 연결리스트 구조.
                         # leaf node에서의 연결리스트를 구현하기 위해 존재함.
        self.isleaf = t_f # 리프노드 인가?
        self.values = [] # 값
        self.keys = [] # 값에 대한 키

    def insert(self, value, key):
        #print(self)
        if (self.values):
            temp = self.values
            if  value in temp:
                print("이미 똑같은 값이 있습니다.")
                return
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
      #  print(self)

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
# '''
# 1. leaf node를 찾는다.
# 2. 값을 삽입한다.
# 3. leaf node의 value의 길이가 degree이면 decompose하고 pnode를 만들어야함.
# 4. 
# '''
    def insert_value(self, value, key):
        '''
        key, value 삽입 과정
        '''
        
        leaf_node = self.find_leaf_node(value) # 해당 값을 넣을 leaf node를 찾아줌.
        leaf_node.insert(value, key) # 해당 leafnode의 고유 함수를 사용해서 value를 삽입함.
        if(len(leaf_node.values) == self.degree):
            # leaf_node에 값을 넣었는데, 이 values의 길이가 degree랑 같으면 decompose가 일어나야함.
            add_leaf_node = node(True)
            add_leaf_node.pkey = leaf_node.pkey
            add_leaf_node.ckey = leaf_node.ckey
            mid_key = int(math.ceil(self.degree /2)) - 1
            add_leaf_node.values = leaf_node.values[mid_key+1:]
            add_leaf_node.keys = leaf_node.keys[mid_key+1:]
            leaf_node.keys = leaf_node.keys[:mid_key+1]
            leaf_node.values = leaf_node.values[:mid_key+1]
            
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
            prior_node.pkey = root_node
            new_node.pkey = root_node
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
                    # 노드를 분리하면서 자식 노드도 같이 옮겨줌.
                    for j in pnode.keys:
                        j.pkey = pnode
                    for j in add_pnode.keys:
                        j.pkey = add_pnode
                    
                    self.new_internal_node(pnode, pnode.values[mid_key], add_pnode)

    def find_leaf_node(self, value):        
        '''
        해당 값이 들어 있을 leaf node를 찾아주는 함수 // 삽입, 삭제 둘 다 사용함.
        '''
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
        print(current_node.keys)
        print(current_node.values)
        return current_node

    def find(self, value, key):
        l = self.find_leaf_node(value)
        for i, item in enumerate(l.values):
            if item == value:
                if key in l.keys[i]:
                    return True
                else:
                    return False
        return False

    
# ---------------------------------------- 삽입 기능 끝 ------------------------------------- 
# -------------------------------------삭제 기능 시작 -----------------------------------
# '''
# 1. 일단 값이 들어가 있을 leaf node를 찾아야함.
# 2. leaf node를 찾고 해당 값과 키를 꺼내야함.
# 3. 꺼내고 나서 해당 leaf node의 value가 pnode의 value에 있다면, pnode의 value도 삭제해주어야함.
# 4. pnode가 비효율적으로 이루어져있다면, merge해야함.
# '''
    def delete(self, value, key):
        leaf_node_for_deletion = self.find_leaf_node(value)
        for num, i in enumerate(leaf_node_for_deletion.values):
            # i 는 단일 값, num은 list안에서의 i값의 순서
            if i == value:
                if key in leaf_node_for_deletion.keys:
                    # 여기까지 왔으면 해당 key와 value가 존재하는데, 삭제 후 노드들을 병합을 하던가
                    # 일반삭제를 해야함. 
                    if leaf_node_for_deletion == self.root_node:
                        #이건 root node만 존재할 때. value, key 삭제
                        leaf_node_for_deletion.values.pop(num)
                        leaf_node_for_deletion.keys.pop(num)
                    else:
                        #이게 지옥임. ㅈㄴ힘들듯
                        #일단 삭제하고, 그 후에 조건 부 함수를 사용해야할듯
                        leaf_node_for_deletion.values.pop(num)
                        leaf_node_for_deletion.keys.pop(num)
                        self.condition_delete(leaf_node_for_deletion, value, key)
                else:
                    print('키가 없음')
            else:
                print("값이 없음")


    def condition_delete(self, node, value, key):
        '''
        1. 만약 leaf_node에서 삭제되는 값이 pnode의 value값이랑 같으면 pnode의 value값이 바뀌어야함
        2. 위에서 바뀌는 pnode의 value는 기존 leafnode에서 가잔 작은 value가 올라가거나
        3. leafnode에 value가 없다면, 그 pnode의 value는 사라져야함.
        4. pnode에 key가 맨 처음에 있다면, pnode의 value값은 옆 노드에서 하나 끌어와야함.
        5. 옆의 node에도 값이 충분하게 있지 않다면, 삭제된 pnode와 이웃 node와 merge가 일어나야함.
        6. 
        '''
        if not node.isleaf:
            # 처음에 들어오는 값은 leafnode이지만 후에 이 함수를 다시 호출하면 internal node이다.
            for i, item in enumerate(node.keys):
                if item == key:
                    node.keys.pop(i)
                    break
            for i, item in enumerate(node.values):
                if item == value:
                    node.values.pop(i)
                    break
        if node == self.root_node and len(node.keys) == 1:
            self.root_node = node.keys[0]
            node.keys[0].pkey = None
            # 자식의 pkey값을 None로 바꿈.
            del node
            return
        elif (len(node.keys) < int(math.ceil(self.degree / 2)) and node.isleaf == False) or (len(node.values) < int(math.ceil((self.degree - 1) / 2)) and node.isleaf == True):
            # redistribute와 merge를 하기 위한 변수 선언.
            condition = 0
            pnode = node.parent
            PrevNode = -1
            NextNode = -1
            PreV = -1
            NextV = -1
            for i, item in enumerate(pnode.keys):
                if item == node:
                    if i > 0:
                        PrevNode = pnode.keys[i - 1]
                        PreV = pnode.values[i - 1]

                    if i < len(pnode.keys) - 1:
                        NextNode = pnode.keys[i + 1]
                        NextV = pnode.values[i]

            if PrevNode == -1:
                neighborNode = NextNode
                value_ = NextV
            elif NextNode == -1:
                condition = 1
                neighborNode = PrevNode
                value_ = PreV
            else:
                if len(node.values) + len(NextNode.values) < self.degree:
                    neighborNode = NextNode
                    value_ = NextV
                else:
                    condition = 1
                    neighborNode = PrevNode
                    value_ = PreV

            if len(node.values) + len(neighborNode.values) < self.degree:
                # merge
                if condition == 0:
                    node_, neighborNode = neighborNode, node
                neighborNode.keys += node_.keys
                if not node_.check_leaf:
                    neighborNode.values.append(value_)
                else:
                    neighborNode.nextKey = node_.nextKey
                neighborNode.values += node_.values

                if not neighborNode.check_leaf:
                    for j in neighborNode.keys:
                        j.parent = neighborNode

                self.condition_delete(node_.parent, value_, node_)
                del node_
            else:
                # redistribute
                if condition == 1:
                    if not node.check_leaf:
                        neighborNodepm = neighborNode.keys.pop(-1)
                        neighborNodekm_1 = neighborNode.values.pop(-1)
                        node.keys = [neighborNodepm] + node.keys
                        node.values = [value_] + node.values
                        pnode = node.parent
                        for i, item in enumerate(pnode.values):
                            if item == value_:
                                p.values[i] = neighborNodekm_1
                                break
                    else:
                        neighborNodepm = neighborNode.keys.pop(-1)
                        neighborNodekm = neighborNode.values.pop(-1)
                        node.keys = [neighborNodepm] + node.keys
                        node.values = [neighborNodekm] + node.values
                        pnode = node.parent
                        for i, item in enumerate(pnode.values):
                            if item == value_:
                                pnode.values[i] = neighborNodekm
                                break
                else:
                    if not node.check_leaf:
                        neighborNodep0 = neighborNode.keys.pop(0)
                        neighborNodek0 = neighborNode.values.pop(0)
                        node.keys = node.keys + [neighborNodep0]
                        node.values = node.values + [value_]
                        pnode = node.parent
                        for i, item in enumerate(pnode.values):
                            if item == value_:
                                pnode.values[i] = neighborNodek0
                                break
                    else:
                        neighborNodep0 = neighborNode.keys.pop(0)
                        neighborNodek0 = neighborNode.values.pop(0)
                        node.keys = node.keys + [neighborNodep0]
                        node.values = node.values + [neighborNodek0]
                        pnode = node.parent
                        for i, item in enumerate(pnode.values):
                            if item == value_:
                                pnode.values[i] = neighborNode.values[0]
                                break

                if not neighborNode.check_leaf:
                    for j in neighborNode.keys:
                        j.parent = neighborNode
                if not node.check_leaf:
                    for j in node.keys:
                        j.parent = node
                if not pnode.check_leaf:
                    for j in pnode.keys:
                        j.parent = pnode
    def root_node_keys(self):
        print("root_node_key", self.root_node.keys)
        


# -----------------------------------삭제 기능 끝 ---------------------------------------
        



# --------------------------------끝----------------------
btree_degree = 4
bptree = b_plus_tree_config(btree_degree)


bptree.insert_value('21','37407')
bptree.insert_value('32','31777')
bptree.insert_value('3','3177')
bptree.insert_value('6','3727')
bptree.insert_value('66','37257')
bptree.insert_value('7','34')
bptree.insert_value('73','34')
bptree.insert_value('5','33')
bptree.insert_value('71','3432')

bptree.insert_value('281','37247')
bptree.root_node_keys()
if(bptree.find('5','33')):
    print("Found")
else:
    print("Not found")
bptree.delete('5','33')

if(bptree.find('5','33')):
    print("Found")
else:
    print("Not found")