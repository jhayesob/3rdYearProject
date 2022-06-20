class ListTree:
    def __init__(self, *args):
        if len(args) == 0:
            # standard instantiation path
            self.objects = []
        else:
            # defined instantiation path
            # args[0] will contain a list terminal node indexes for when we need to make a predefined trie
            # args[1] will take in a list of data objects to be stored at each terminal node
            self.objects = []
            terminal_nodes_list = args[0]  # no reason for this line...
            for i in range(len(terminal_nodes_list)):
                # using 'for i in range(len(_LIST_))' allows me to iterate over the list elements while keeping track of
                # their position in the list
                subscript = []
                for n in range(len(terminal_nodes_list[i])):
                    subscript.append(terminal_nodes_list[i][n])
                    try:
                        if type(self[subscript[:n + 1]]) is list:
                            # (f'Node exists at index: {subscript[:n + 1]} and holds a list')
                            pass  # aim of this algorithm is to check if a list is held at each element that it should.
                            # so if a list exists at this element, we merely progress through to the next iteration
                        elif type(self[subscript[:n + 1]]) is int:
                            # print(f'-------- Node exists at index: {subscript[:n + 1]} and holds a Hand**')
                            pass
                        else:
                            # print(f'A Node does not exist at index: {subscript[:n + 1]}')
                            raise IndexError
                        # let's check if querying if an object exists here produces a none result. if that f string
                        # prints out True, I can generify the input object. if not then I'll just specify
                    except IndexError:
                        if subscript == [0]:
                            # adding first two nodes because this algorithm is built to work on a trie structure with at
                            # least the first two nodes having been initialised

                            if terminal_nodes_list[i] == [0] and terminal_nodes_list[-1] != [1]:
                                self.objects.extend([args[1][i], []])
                            elif terminal_nodes_list[i] == [0] and terminal_nodes_list[-1] == [1]:
                                self.objects.extend([args[1][i], args[1][-1]])
                            elif terminal_nodes_list[i] != [0] and terminal_nodes_list[-1] == [1]:
                                self.objects.extend([[], args[1][-1]])
                            else:
                                self.objects.extend([[], []])
                            # print(f'first two child nodes are added to tree to make it operable')
                        elif subscript == [1]:
                            # this bit actually shouldn't be reachable theoretically, because this scenario should have
                            # been made impossible when the first two branches were added to make the tree operable
                            pass
                        else:
                            amended_sub_script = subscript[:-1]
                            amended_sub_script.append(1)
                            if n == len(terminal_nodes_list[i]) - 1:  # checking to see if terminal node at this level
                                # adding -1 because n is a zero indexed variable but len is not.
                                # print("-- Entered adding terminal node level")
                                if subscript[n] == 0:  # if subscript is in "xx0" format, then check if
                                    # terminal_nodes_list[i+1] is equal to subscript with its last char replaced with 1
                                    if terminal_nodes_list[i + 1] == amended_sub_script:
                                        # actually I think ive gotta handle the case in which this is the last terminal
                                        # node... cos then term...[i+1] should make an index error
                                        self[subscript[:n]] = [args[1][i], args[1][i + 1]]
                                        # print(f'--- Inserted 2 hand nodes at {subscript} and at {amended_sub_script}')
                                    else:
                                        self[subscript[:n]] = [args[1][i], []]
                                        # print(f'--- Inserted 1 hand node at {subscript}')
                                    # improves algorithm efficiency by checking if it needs to insert a Hand object in
                                    # the position to the right, rather than dealing with the insertion of that node in
                                    # the next iteration
                            else:
                                if len(terminal_nodes_list[i + 2]) == len(terminal_nodes_list[i]) - 1:
                                    self[subscript[:n]] = [[], args[1][i + 2]]
                                    # print(f'--- Inserted 1 list node at {subscript} and 1 object at {
                                    # amended_sub_script}')
                                else:
                                    # print(f'--- Inserted 2 child lists at {subscript[:n]}')
                                    self[subscript[:n]] = [[], []]
                            # since no node holding a list exists at the coordinate addressed by subscript[:n], I assign
                            # list or int nodes to be held children by the existing list at subscript[:n-1].

    def __getitem__(self, key):
        # takes a list where the elements make up the index of the target item in this structure.
        if len(key) == 1:
            return self.objects[key[0]]
        elif len(key) == 2:
            return self.objects[key[0]][key[1]]
        elif len(key) == 3:
            return self.objects[key[0]][key[1]][key[2]]

    def __setitem__(self, key, value):
        if len(key) == 1:
            self.objects[key[0]] = value
        elif len(key) == 2:
            self.objects[key[0]][key[1]] = value
        elif len(key) == 3:
            self.objects[key[0]][key[1]][key[2]] = value

    def get_list_tree(self):
        return self.objects

    def add_children_to_tree(self, parent_node_index, new_hand1, new_hand2):
        if type(parent_node_index) is list:
            if (len(parent_node_index) == 0) or (type(self[parent_node_index]) is not list):
                # overwrite current data at that point to now contain a list of the two split hands
                if len(parent_node_index) == 0:
                    self.objects.extend([new_hand1, new_hand2])
                else:
                    self[parent_node_index] = [new_hand1, new_hand2]
            else:
                print("ERROR: wrong type at self.hands[parentNodeIndex]")
                print(parent_node_index)
                print(self[parent_node_index])
        else:
            print("ERROR: wrong type passed to parentNodeIndex")

    def get_trie_terminal_indexes(self):
        return ListTree.bubble_sort(self.trie_traversal())

    def trie_traversal(self, *args):
        # args[0] = index of node to start on aka: current_node
        # args[1] = [list of next indexes to visit]
        # args[2] = [list of terminal node indexes]
        if len(args) == 0:
            nodes_to_visit = [[0], [1]]
            return self.trie_traversal([0], nodes_to_visit)
        else:
            if len(args) == 3:
                terminal_node_indexes = args[2]
            else:
                terminal_node_indexes = []
            args[1].remove(args[0])  # this node is marked as visited by removing its index from args[1]
            if type(self[args[0]]) is list:
                for x in (0, 1):
                    args[1].append(args[0] + [x])
                return self.trie_traversal(args[1][0], args[1], terminal_node_indexes)
            else:
                terminal_node_indexes.append(args[0])
                if len(args[1]) == 0:  # return data - no nodes left to visit
                    return terminal_node_indexes
                else:
                    return self.trie_traversal(args[1][0], args[1], terminal_node_indexes)

    @staticmethod
    def comparator(l_index_1, l_index_2):
        if len(l_index_1) < len(l_index_2):
            r = len(l_index_1)
        elif len(l_index_1) == len(l_index_2):
            r = len(l_index_1)
        else:
            r = len(l_index_2)
        for i in range(r):
            if l_index_1[i] > l_index_2[i]:
                return 1
            elif l_index_1[i] < l_index_2[i]:
                return -1
        return 0

    @staticmethod
    def bubble_sort(indexes):
        # trie_data[0] holds list of positional indexes
        # trie_data[1] holds list of objects at these indexes
        n = len(indexes)
        for i in range(n):
            for j in range(0, n - i - 1):
                if ListTree.comparator(indexes[j], indexes[j + 1]) == 1:
                    indexes[j], indexes[j + 1] = indexes[j + 1], indexes[j]
        return indexes
