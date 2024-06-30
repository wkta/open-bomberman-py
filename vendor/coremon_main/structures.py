from abc import ABCMeta, abstractmethod


class Stack:
    def __init__(self, given_seq=None):
        if given_seq is None:
            self.fifo_list = []
        else:
            self.fifo_list = list(given_seq)

    def push(self, element):
        self.fifo_list.append(element)
        # - debug
        # print()
        # print('PUSH')
        # print('etat de pile {}'.format(self.fifo_list))

    def top_down_trav(self):
        return reversed(self.fifo_list)

    def bottom_up_trav(self):
        return self.fifo_list

    def pop(self):
        try:
            tmp = self.fifo_list.pop()
            res = tmp
        except IndexError:
            res = None  # the stack's already empty

        # - debug
        # print()
        # print('POP')
        # print('etat de pile {}'.format(self.fifo_list))

        return res

    def peek(self):
        try:
            return self.fifo_list[-1]
        except IndexError:
            return None  # the stack's empty

    def count(self):
        return len(self.fifo_list)


class BaseGameState(metaclass=ABCMeta):
    
    def __init__(self, state_ident, state_name):
        self.__state_ident = state_ident
        self.__state_name = state_name

    def get_id(self):
        return self.__state_ident

    def get_name(self):
        return self.__state_name

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def release(self):
        pass

    def resume(self):
        print(self.__class__.__name__)
        raise AssertionError('not meant to be resumed')

    def pause(self):
        print(self.__class__.__name__)
        raise AssertionError('not meant to be paused')


class Tree:
    def __init__(self, root_content):
        self.root = TreeNode(root_content, None)
        self.__allnodes = set()
        self.__allnodes.add(self.root)
    
    def add_content(self, content, parent_node):
        if parent_node not in self.__allnodes:
            raise ValueError('cannot find specified parent_node')
        
        n = TreeNode(content, parent_node)
        parent_node.childs.append(n)
        self.add_node(n)
    
    def count(self):
        return len(self.__allnodes)
    
    def get_node_by_content(self, searched_content):
        queue = [self.root]
        while len(queue) > 0:
            exn = queue.pop()
            if searched_content == exn.content:
                return exn
            if not exn.is_leaf():
                queue.extend(exn.childs)
        return None

    def cut_from_node(self, ref_node):
        if ref_node == self.root:
            raise ValueError('empty tree not allowed')

        if not ref_node.is_leaf():
            # if node has childs, we shall cut the whole branch
            for c in ref_node.childs:
                self.cut_from_node(c)

        ref_node.parent.childs.remove(ref_node)
        self.__allnodes.remove(ref_node)


class TreeNode:
    def __init__(self, content, parent):
        self.childs = list()
        self.content = content
        self.parent = parent
        
    def is_leaf(self):
        return len(self.childs) == 0
