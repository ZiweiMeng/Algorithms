'''
The file contains the adjacency list representation of a simple undirected graph. There are 200 vertices labeled 1 to 200. The first column in the file represents the vertex label, and the particular row (other entries except the first column) tells all the vertices that the vertex is adjacent to. So for example, the 6^{th}6 
th
  row looks like : "6	155	56	52	120	......". This just means that the vertex with label 6 is adjacent to (i.e., shares an edge with) the vertices with labels 155,56,52,120,......,etc

Your task is to code up and run the randomized contraction algorithm for the min cut problem and use it on the above graph to compute the min cut. (HINT: Note that you'll have to figure out an implementation of edge contractions. Initially, you might want to do this naively, creating a new graph from the old every time there's an edge contraction. But you should also think about more efficient implementations.) (WARNING: As per the video lectures, please make sure to run the algorithm many times with different random seeds, and remember the smallest cut that you ever find.) Write your numeric answer in the space provided. So e.g., if your answer is 5, just type 5 in the space provided.
'''
import sys
import random
import numpy as np 
from datetime import datetime


class ComputeMinCut():
    '''
    compute min cut, return #k and partitions
    '''
    def __init__(self, adjacency_list):
        self.adjacency_list_ = adjacency_list

    def convert_adjacency_list(self):
        '''
        convert input into appropriate structure
        '''
        adjacency_list = {}
        partition_dic = {}
        for vs in self.adjacency_list_:
            # print(vs)
            adjacency_list[vs[0]] = vs[1:]
            partition_dic[vs[0]] = set()
        return adjacency_list, partition_dic

    def fuse_step(self, adjacency):
        '''
        adjacency list is a dictionary mapping v to list of connected vertice
        partition_dic is a dictionary mapping v to all fused vertice with it
        '''
        adjacency_list, partition_dic = adjacency

        # randomly choose 2 different vertice in set
        a,b = random.sample(list(adjacency_list.keys()),2)
        if a<b:
            fused = a
            to_fuse = b
        elif a>b:
            fused = b
            to_fuse = a 
        else:
            raise ValueError

        # fuse
        # check if any other vertex linked to to_fuse, and replace it by fused
        for v in adjacency_list:
            if to_fuse in adjacency_list[v]:
                adjacency_list[v].remove(to_fuse)
                adjacency_list[v].append(fused)
        # delete self-loop
        if fused in adjacency_list[fused]:
            adjacency_list[fused].remove(fused)
        # connect any vertice that previously only linked to to_fuse to fused
        for v in adjacency_list[to_fuse]:
            if v!=fused: # avoid self-loop
                adjacency_list[fused].append(v)
        # remove to_fuse 
        adjacency_list.pop(to_fuse)

        # update partitions
        partition_dic[fused].add(to_fuse)
        partition_dic[fused] = partition_dic[to_fuse].union(partition_dic[fused])
        partition_dic.pop(to_fuse)
        # print('adjacency',adjacency_list)

        adjacency = (adjacency_list, partition_dic)
        return adjacency

    def fuse(self):
        '''
        fuse all N vertice in N-2 steps into 2 groups
        '''
        # self.convert_adjacency_list()
        adjacency_list, partition_dic  = self.convert_adjacency_list()
        # print('new fuse iter adj', adjacency_list)

        random.seed(datetime.now())
        temp = list(adjacency_list.keys())
        random.shuffle(temp)
        adjacency_list = {k:adjacency_list[k] for k in temp}
        temp = list(partition_dic.keys())
        random.shuffle(temp)
        partition_dic = {k:partition_dic[k] for k in temp}

        adjacency = (adjacency_list, partition_dic)

        n = len(adjacency_list)
        for _ in range(n-2):
            adjacency = self.fuse_step(adjacency)
        final_adj_list, final_partition = adjacency
        assert len(final_partition)==2, 'partition is not finished with %d vertice left!'%len(final_partition)
        k = len(list(final_adj_list.values())[0])
        return k, final_partition

    def iter_optimal(self, iter=10):
        '''
        iterate #iter different min cut search to find the global optimal
        '''
        random.seed(datetime.now())
        best_k = 99999
        best_partition = None

        for _ in range(iter):
            k,final_partition = self.fuse()
            # print(k)
            # print(best_k)
            if k<best_k:
                best_k = k 
                best_partition = final_partition

        return best_k, best_partition

if __name__ == "__main__":
    filename = sys.argv[1]
    print(filename)
    with open(filename) as f:
        list_of_lists = f.readlines()

    # print(list_of_lists[-10:])
    adj_lists = []
    for line in list_of_lists:
        adj_lists.append([int(x) for x in line.split()])
    # print(adj_lists[-3:])
    cmc = ComputeMinCut(adj_lists)
    # cmc.convert_adjacency_list()
    # print(list(cmc.adjacency_list.keys())[-3:])
    # print(list(cmc.adjacency_list.values())[-3:])
    # print(cmc.adjacency_list[-10:])
    n = len(adj_lists)
    iter = int(n**2*np.log(n))
    print(iter)

    best_k, best_partition = cmc.iter_optimal(iter=5500)
    print(best_k)
    print(best_partition)
    # print(sum([len(v) for v in best_partition.values()]))
    # print(len(best_partition[1]))
    
