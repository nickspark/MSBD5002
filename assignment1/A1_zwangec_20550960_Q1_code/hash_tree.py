def build_hash_tree(datas, max_leaf_size = 3, depth = 0):
    '''
    :param datas: the whole dataset list[list]
    :param max_leaf_size: max number of a leaf, the edge condition of
    generating 3 new leaves
    :param depth: the depth of the tree, representing the ith number to judge
    :return: the final result represented in []
    '''
    res = [[], [], []]
    for data in datas:
        res[(data[depth] + 2) % 3].append(data)
    for i in range(len(res)):
        # print child
        if len(res[i]) > max_leaf_size:
            #recursion to generate new 3 leaves
            res[i] = build_hash_tree(res[i], depth=depth + 1)
    return res



if __name__ == '__main__':
    datas = '{1 2 4}, {1 2 9}, {1 3 5}, {1 3 9}, {1 4 7}, {1 5 8}, {1 6 7}, {1 7 9}, {1 8 9}, {2 3 5}, {2 4 7}, {2 5 6}, {2 5 7}, {2 5 8}, {2 6 7}, {2 6 8}, {2 6 9}, {2 7 8}, {3 4 5}, {3 4 7}, {3 5 7}, {3 5 8}, {3 6 8}, {3 7 9}, {3 8 9}, {4 5 7}, {4 5 8}, {4 6 7}, {4 6 9}, {4 7 8}, {5 6 7}, {5 7 9}, {5 8 9}, {6 7 8}, {6 7 9}'
    datas = datas.split(', ')
    #transfer original data to list[list]
    res = map(lambda x:list(map(int, x.strip('}').strip('{').split(' '))), datas)
    print (res)
    #test set
    #res = [[1,4,5],[1,2,4],[4,5,7],[1,2,5],[4,5,8],[1,5,9],[1,3,6],[2,3,4],[5,6,7],[3,4,5],[3,5,6],[3,5,7],[6,8,9],[3,6,7],[3,6,8]]
    t = build_hash_tree(res)
    print (t)






