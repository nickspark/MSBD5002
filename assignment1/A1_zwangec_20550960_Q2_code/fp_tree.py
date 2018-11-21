import pandas as pd
import csv
import numpy as np

class fp_node:
    def __init__(self, item, degree, parent):
        self.item = item
        self.degree = degree
        self.parent = parent
        self.link_node = None
        self.children = {}


class fp_tree:
    '''
    the fp tree class
    '''
    def __init__(self, item_set):
        '''
        :param item_set: the dataset
        '''
        self.item_set = item_set




    def build_tree(self, df):
        '''
        :param df: the dataset
        :return: the root of the tree and the head table of the dataset
        headtable: a dict including the item(key) degree(value[0]) node(value[1])
        '''
        root = fp_node('null set', 1, None)
        head_table = self.figure_freq(df)
        for trans, degree in df.items():
            temp = {}
            for item in trans:
                if item in head_table:
                    temp[item] = head_table[item][0]
            if len(temp) > 0:
                orderedItems = sorted(temp, key=temp.get, reverse=True)
                self.update_tree(orderedItems, head_table, root,  degree)
        return root, head_table


    def figure_freq(self, item_set):
        '''

        :param item_set: the dataset
        :return: the head table
        using this function to figure out the head table
        '''
        head_table = {}
        for trans in item_set:
            num = item_set[trans]
            while num:
                for item in trans:
                    head_table[item] = head_table.get(item, 0) + 1
                num -= 1
        #print(head_table['whole milk'])
        for key in set(head_table.keys()):
            if head_table[key] < 300:
                del head_table[key]

        for key in head_table:
            value = head_table[key]
            head_table[key] = [value, None]
        return head_table


    def update_tree(self, item_list, head_table, root, degree):
        '''

        :param item_list: the new dataset
        :param head_table: head table storing item,degree and node
        :param root: the root
        :param degree: the degree of the item
        :return:
        '''

        if item_list[0] in root.children:
            root.children[item_list[0]].degree += degree
        else:
            root.children[item_list[0]] = fp_node(item_list[0], degree, root)
            if head_table[item_list[0]][1] == None:
                head_table[item_list[0]][1] = root.children[item_list[0]]
            else:
                node = head_table[item_list[0]][1]
                while(node.link_node != None):
                    node = node.link_node
                node.link_node = root.children[item_list[0]]
        if len(item_list) > 1:
            self.update_tree(item_list[1:], head_table, root.children[item_list[0]], degree)

        return head_table


    def traverse(self, fp_node):
        '''

        :param fp_node: the item node we want to build frequen item tree
        :return: the frequent pairs
        '''
        res = {}
        while fp_node != None:
            temp_node = fp_node
            path = []
            while temp_node.parent != None:
                path.append(temp_node.item)
                temp_node = temp_node.parent
            # print(path)
            if len(path) > 1:
                res[frozenset(path[1:])] = fp_node.degree

            fp_node = fp_node.link_node
        #print(res)
        return res


    def prune(self, root, head_table, pre_fix, freq_itemset, root_set):
        '''

        :param root: tree's root
        :param head_table: head table storing item,degree and node
        :param pre_fix: prefix of the new item
        :param freq_itemset: the frequent itemset result
        :param root_set: to store all the root of the frequent trees
        to build the conditional trees of all frequent items
        '''
        #print(head_table)
        for item in head_table.keys():
            temp = pre_fix.copy()
            temp.add(item)
            freq_itemset.append(temp)
            new_dataset = self.traverse(head_table[item][1])
            new_root, new_head = self.build_tree(new_dataset)
            root_set.append(new_root)
            if new_head != None:
                self.prune(new_root, new_head, temp, freq_itemset, root_set)


    def find_tree(self, node, tree):
        '''
        Q2
        :param node: the root of the conditional tree
        :param tree: the result list
        '''
        if fp_node != None:
            tree.append([node.item+'    '+str(node.degree)])
            if node.children != None:
                #tree.append([])
                for child in node.children:
                    self.find_tree(node.children[child], tree)



if __name__ == '__main__':
    '''
    to transfer the data to {frozenset:time}
    '''
    #process the data
    with open('groceries.csv') as f:
        data = list(csv.reader(f))
    item_set = {}
    for row in data[:]:
        while '' in row:
            row.remove('')
        row = frozenset(i for i in row)
        item_set[row] = item_set.get(row, 0) + 1
    tree = fp_tree(item_set)
    root, head_table = tree.build_tree(item_set)
    # print(head_table)
    freq_itemset = []
    pre_fix = set([])
    root_set = []
    tree.prune(root, head_table, pre_fix, freq_itemset, root_set)
    with open("output.csv", "w") as f:
        writer = csv.writer(f)
        for item in freq_itemset:
            writer.writerow([item])
            #print(item)
    #find all the conditional trees
    for root in root_set:
        res = []
        tree.find_tree(root, res)
        if len(res) > 2:
            print(res)







