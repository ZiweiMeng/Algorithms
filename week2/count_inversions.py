import numpy as np 
from time import time
import sys

class countInversions():
    '''
    count number of inversions in an array of integers
    '''
    def __init__(self):
        '''
        input: arr is an array of integers
        '''
        pass

    def count_split_and_merge(self, arrs=None):
        '''
        input: arrs is a list contains 2 sorted arrays
        output: return number of inversions in splits and merged sorted array
        '''
        left_arr, right_arr = arrs
        left_size = len(left_arr)
        right_size = len(right_arr)
        merged_arr = np.zeros(left_size+right_size) # initialize merged array by zeros
        split_inversions = 0


        i = j = k = 0
        while i<left_size and j<right_size:
            if left_arr[i]<=right_arr[j]:
                merged_arr[k] = left_arr[i]
                i += 1
            else:
                merged_arr[k] = right_arr[j]
                j += 1
                split_inversions += (left_size - i)
            k += 1
        if i<left_size: # right_arr all copied to merged while left_arr still not
            assert len(merged_arr[k:])==len(left_arr[i:])
            merged_arr[k:] = left_arr[i:]
        if j<right_size: # left_arr all copied to merged while right_arr still not
            assert len(merged_arr[k:])==len(right_arr[j:])
            merged_arr[k:] = right_arr[j:]
        
        return split_inversions, merged_arr

    def count_inversions(self, arr=None):
        '''
        input: array of integers
        output: return count of inversions in array and sorted array
        '''
        if len(arr) in [0,1]: # [] or [#one int] don't have inversions
            return 0, arr
        if len(arr)==2:
            return int(arr[0]>arr[1]), np.sort(arr)
        
        n = len(arr)
        half_n = int(n/2)
        left_arr, right_arr = arr[:half_n], arr[half_n:]
        left_inversions, left_sorted = self.count_inversions(left_arr)
        right_inversions, right_sorted  = self.count_inversions(right_arr)
        split_inversions, merged_sorted = self.count_split_and_merge(arrs=[left_sorted, right_sorted])
        return left_inversions+right_inversions+split_inversions, merged_sorted

    def compute(self, arr=None):
        '''
        input: array of intergers
        output: return count of inversions in array
        '''
        inversions, _ = self.count_inversions(arr)
        return inversions


        




if __name__ == "__main__":
    # # test count_split_and_merge
    # arr = np.array([6,5,4,3,2])
    # arrs = [np.array([4,5,6]), np.array([2,3])]
    # inv_cnt = countInversions()
    # print(inv_cnt.count_split_and_merge(arrs))

    # # test count_inversions
    # arr = np.array([6,5,4,3,2])
    # inv_cnt = countInversions()
    # print(inv_cnt.count_inversions(arr))

    # # test compute
    # arr = np.array([3,2,4,5,1])
    # inv_cnt = countInversions()
    # st = time()
    # print(inv_cnt.compute(arr))
    # ed = time()
    # print('estimated computing time for %d-length array: %.3fs'%(len(arr), ed - st))

    # read in text file
    filename = sys.argv[1]
    print(filename)
    with open(filename) as f:
        intList = f.readlines()
    intList = [int(x.strip()) for x in intList]
    arr = np.array(intList)
    inv_cnt = countInversions()
    st = time()
    print(inv_cnt.compute(arr))
    ed = time()
    print('estimated computing time for %d-length array: %.3fs'%(len(arr), ed - st))


