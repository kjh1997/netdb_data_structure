# B+ tee in python


import math

# Node creation
class Node:
    def __init__(self, order):
        self.order = order
        self.values = []
        self.keys = []
        self.nextKey = None
        self.parent = None
        self.check_leaf = False

    # Insert at the leaf
    def insert_at_leaf(self, leaf, value, key):
        if (self.values):
            temp1 = self.values
            for i in range(len(temp1)):
                if (value == temp1[i]):
                    self.keys[i].append(key)
                    break
                elif (value < temp1[i]):
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    break
                elif (i + 1 == len(temp1)):
                    self.values.append(value)
                    self.keys.append([key])
                    break
        else:
            self.values = [value]
            self.keys = [[key]]


# B plus tree
class BplusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.check_leaf = True

    # Insert operation
    def insert(self, value, key):
        value = str(value)
        old_node = self.search(value)
        old_node.insert_at_leaf(old_node, value, key)

        if (len(old_node.values) == old_node.order):
            node1 = Node(old_node.order)
            node1.check_leaf = True
            node1.parent = old_node.parent
            mid = int(math.ceil(old_node.order / 2)) - 1
            node1.values = old_node.values[mid + 1:]
            node1.keys = old_node.keys[mid + 1:]
            node1.nextKey = old_node.nextKey
            old_node.values = old_node.values[:mid + 1]
            old_node.keys = old_node.keys[:mid + 1]
            old_node.nextKey = node1
            self.insert_in_parent(old_node, node1.values[0], node1)

    # Search operation for different operations
    def search(self, value):
        current_node = self.root
        while(current_node.check_leaf == False):
            temp2 = current_node.values
            for i in range(len(temp2)):
                if (value == temp2[i]):
                    current_node = current_node.keys[i + 1]
                    break
                elif (value < temp2[i]):
                    current_node = current_node.keys[i]
                    break
                elif (i + 1 == len(current_node.values)):
                    current_node = current_node.keys[i + 1]
                    break
        return current_node

    # Find the node
    def find(self, value, key):
        l = self.search(value)
        for i, item in enumerate(l.values):
            if item == value:
                if key in l.keys[i]:
                    return True
                else:
                    return False
        return False

    # Inserting at the parent
    def insert_in_parent(self, n, value, ndash):
        if (self.root == n):
            rootNode = Node(n.order)
            rootNode.values = [value]
            rootNode.keys = [n, ndash]
            self.root = rootNode
            n.parent = rootNode
            ndash.parent = rootNode
            print(rootNode.keys)
            return

        parentNode = n.parent
        temp3 = parentNode.keys
        for i in range(len(temp3)):
            if (temp3[i] == n):
                parentNode.values = parentNode.values[:i] + \
                    [value] + parentNode.values[i:]
                parentNode.keys = parentNode.keys[:i +
                                                  1] + [ndash] + parentNode.keys[i + 1:]
                if (len(parentNode.keys) > parentNode.order):
                    parentdash = Node(parentNode.order)
                    parentdash.parent = parentNode.parent
                    mid = int(math.ceil(parentNode.order / 2)) - 1
                    parentdash.values = parentNode.values[mid + 1:]
                    parentdash.keys = parentNode.keys[mid + 1:]
                    value_ = parentNode.values[mid]
                    if (mid == 0):
                        parentNode.values = parentNode.values[:mid + 1]
                    else:
                        parentNode.values = parentNode.values[:mid]
                    parentNode.keys = parentNode.keys[:mid + 1]
                    for j in parentNode.keys:
                        j.parent = parentNode
                    for j in parentdash.keys:
                        j.parent = parentdash
                    self.insert_in_parent(parentNode, value_, parentdash)

    # Delete a node
    def delete(self, value, key):
        node_ = self.search(value)

        temp = 0
        for i, item in enumerate(node_.values):
            if item == value:
                temp = 1

                if key in node_.keys[i]:
                    if len(node_.keys[i]) > 1:
                        # 그냥 값만 삭제
                        node_.keys[i].pop(node_.keys[i].index(key))
                        print(node_.keys[i].pop(node_.keys[i].index(key)))
                    elif node_ == self.root:
                        # root node에서 삭제
                        node_.values.pop(i)
                        node_.keys.pop(i)
                        print(node_.keys.pop(i))
                        print(node_.values.pop(i))
                    else:
                        # 노드가 삭제 될 경우.
                        node_.keys[i].pop(node_.keys[i].index(key))
                        del node_.keys[i]
                        node_.values.pop(node_.values.index(value))
                        # 삭제 후 들어감.
                        self.deleteEntry(node_, value, key)
                else:
                    print("Value not in Key")
                    return
        if temp == 0:
            print("Value not in Tree")
            return

    # Delete an entry
    def deleteEntry(self, node_, value, key):

        if not node_.check_leaf: # 리프노드가 아니면 >> internal node # 아까 만약에 leaf node 를 삭제하고 pnode가 여기에 들어왔으면
                                                                     #여기서 삭제한 leaf node 에 해당하는  key를 삭제함. 마찬가지로 해당하는 value도 삭제함.
            for i, item in enumerate(node_.keys):
                if item == key:
                    node_.keys.pop(i)
                    break
            for i, item in enumerate(node_.values):
                if item == value:
                    node_.values.pop(i)
                    break

        if self.root == node_ and len(node_.keys) == 1:
            # 노드가 루트노드이고 키가 1개 // 루트노드면 그냥 삭제하면 됨.
            self.root = node_.keys[0]
            node_.keys[0].parent = None
            del node_
            return

        elif (len(node_.keys) < int(math.ceil(node_.order / 2)) and node_.check_leaf == False) or (len(node_.values) < int(math.ceil((node_.order - 1) / 2)) and node_.check_leaf == True):
                # (노드의 키가  degree/2보다 작고, 노드가 internal node) or (노드의 값의 길이 < (degree-1)/2 이고, 노드가 leaf node)
                # ex) internal node가 
            is_predecessor = 0
            parentNode = node_.parent # 직속 상위 노드
            PrevNode = -1
            NextNode = -1
            PrevK = -1
            PostK = -1
            for i, item in enumerate(parentNode.keys):
                # pnode에서 키(자식노드(degree = 3 일 경우 key는 3개까지 존재 가능))

                if item == node_:
                    # current node와 pnode의 item(key)가 같으면 
                    # 이웃(앞, 뒤) 을 찾아줘야함.
                    #  |    k1  |v| k2  |v|  k3  ㅣ
                    if i > 0:
                        # 자신과 같은 depth에 위치한 이웃(뒤에 위치)한 노드
                        #  pnode |    k1  |v1| k2  |v2|  k3  ㅣ
                        PrevNode = parentNode.keys[i - 1] # k1
                        PrevK = parentNode.values[i - 1]  # v1

                    if i < len(parentNode.keys) - 1: # i가 부모키의 길이보다 1이 작아야함. 이유는 degree가 3일 경우 value는 2개, key는 3개까지 가질 수 있음.
                                                     #  #앞에 위치한 노드
                        NextNode = parentNode.keys[i + 1] # k3 or k2
                        PostK = parentNode.values[i]      # v2 or v1

            if PrevNode == -1:
                # 위에서 이웃 노드를찾았는데 이전에 위치한 노드가 없으면
                ndash = NextNode
                value_ = PostK
            elif NextNode == -1:
                # 위에서 이웃 노드를찾았는데 앞에 위치한 노드가 없으면
                is_predecessor = 1
                ndash = PrevNode    # k3 or k2
                value_ = PrevK      # v2 or v1
            else:
                # 둘 다 위치한 경우
                if len(node_.values) + len(NextNode.values) < node_.order:
                    # 현재 노드의 값의 길이랑 앞에 위치한 노드의 값의 길이의 합이 degree보다 작을 경우. >> 비효율적이므로, merge가 일어나야하므로, 밑에 
                    ndash = NextNode
                    value_ = PostK
                else:
                    
                    is_predecessor = 1
                    ndash = PrevNode
                    value_ = PrevK

            if len(node_.values) + len(ndash.values) < node_.order:
                # 위에서 merge가 필요한 node를 골라 ndash와 value에 각 담았다. 이제 merge를 진행한다.
                #  |    k1  |v| k2  |v|  k3  ㅣ
                # k2(node)랑 k3(ndash)랑 merge작업  // k3삭제
                if is_predecessor == 0:
                    node_, ndash = ndash, node_
                    # ndash에 있는 key
                ndash.keys += node_.keys
                if not node_.check_leaf:
                    ndash.values.append(value_)
                else:
                    ndash.nextKey = node_.nextKey
                ndash.values += node_.values

                if not ndash.check_leaf:
                    for j in ndash.keys:
                        j.parent = ndash

                self.deleteEntry(node_.parent, value_, node_)
                # 노드의 상위 노드를 건드려야함. 
                # 낭비되는 공간을 삭제 후 부모 노드를 삭제한다. 부모 노드를 다시 조건부 삭제 함수에 넣는다.
                del node_
            else:
                # 여기까지 오면 값들과 키 들은 다 삭제가 되어있다.
                # 이 else문에서 하는 역할은
                if is_predecessor == 1:
                    # 이 경우는 pre, next node가 둘 다 있기는 하지만, next node의 value 의 길이와  현재 노드의 길이의 합이 degree보다 작을 경우이거나, // pre node와 next node 둘 다 없을 경우에 해당함.
                    if not node_.check_leaf:
                        # internal node
                        ndashpm = ndash.keys.pop(-1) # 맨 끝의 키를 뽑음.
                        ndashkm_1 = ndash.values.pop(-1) #  맨 끝의 값을 뽑음
                        
                        node_.keys = [ndashpm] + node_.keys 
                        node_.values = [value_] + node_.values
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashkm_1
                                break
                    else:
                        # leaf node
                        ndashpm = ndash.keys.pop(-1)
                        ndashkm = ndash.values.pop(-1)
                        node_.keys = [ndashpm] + node_.keys
                        node_.values = [ndashkm] + node_.values
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashkm
                                break
                else:
                    if not node_.check_leaf:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [value_]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashk0
                                break
                    else:
                        ndashp0 = ndash.keys.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node_.keys = node_.keys + [ndashp0]
                        node_.values = node_.values + [ndashk0]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndash.values[0]
                                break

                if not ndash.check_leaf:
                    for j in ndash.keys:
                        j.parent = ndash
                if not node_.check_leaf:
                    for j in node_.keys:
                        j.parent = node_
                if not parentNode.check_leaf:
                    for j in parentNode.keys:
                        j.parent = parentNode


# Print the tree
def printTree(tree):
    lst = [tree.root]
    level = [0]
    leaf = None
    flag = 0
    lev_leaf = 0

    node1 = Node(str(level[0]) + str(tree.root.values))

    while (len(lst) != 0):
        x = lst.pop(0)
        lev = level.pop(0)
        if (x.check_leaf == False):
            for i, item in enumerate(x.keys):
                print("1",item.values)
        else:
            for i, item in enumerate(x.keys):
                print("1", item.values)
            if (flag == 0):
                lev_leaf = lev
                leaf = x
                flag = 1

def all_node(tree):
    print(tree.root)
    leaf = []
    for num, i in enumerate(tree.root.keys):
        print(num, i.keys)
        for j in i.keys:
            print("??",j.keys)
            
            # for k in j.keys:
            #     print(k)
      
    print(leaf)

record_len = 3
bplustree = BplusTree(record_len)
bplustree.insert('5', '33')
bplustree.insert('15', '33')
bplustree.insert('25', '31')
bplustree.insert('35', '41')
bplustree.insert('45', '10')
bplustree.insert('562', '35')
bplustree.insert('1523', '26')
bplustree.insert('251', '37')
bplustree.insert('355', '48')
bplustree.insert('4125', '19')
bplustree.delete('5','33')
bplustree.delete('562', '35')
bplustree.delete('1523', '26')
bplustree.delete('251', '37')
bplustree.delete('355', '48')
bplustree.delete('4125', '19')
bplustree.delete('15', '33')
bplustree.delete('25', '31')
bplustree.delete('35', '41')
bplustree.delete('45', '10')


#printTree(bplustree)

# if(bplustree.find('5', '34')):
#     print("Found")
# else:
#     print("Not found")