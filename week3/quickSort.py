import numpy as np 
from time import time
import sys

class quickSort():
    '''
    Sort an n-length array by quickSort algorithm
    Compute number of comparisons all recursions made
    '''
    def __init__(self, arr=None, choose_pivot='first'):
        '''
        pass parameters
        '''
        self.arr_ = arr
        assert (choose_pivot in ['first','last','median']), 'Invalid pivot choosen method!'
        self.choose_pivot_ = choose_pivot
        self.comparisons_ = 0

    def choose_pivot(self, arr):
        '''
        choose pivot by 3 different methods
        '''
        if self.choose_pivot_=='first':
            pass # since first element is already our pivot, do nothing
        elif self.choose_pivot_=='last':
            temp = arr[-1]
            arr[-1] = arr[0]
            arr[0] = temp # exchange last and first element in array
        elif self.choose_pivot_=='median':
            mid = int((len(arr)-1)/2)
            triplet = [arr[0],arr[mid],arr[-1]]
            med = np.median(triplet)
            if med==arr[0]:
                med_i = 0
            elif med==arr[-1]:
                med_i = -1
            else:
                med_i = mid
            arr[med_i] = arr[0]
            arr[0] = med # exchange median item and first element in array
        else:
            raise ValueError
        
        return arr

    def partition_by_pivot(self, arr):
        if len(arr)<=1:
            self.comparisons_ += 0
        else:
            self.comparisons_ += (len(arr)-1)

        if len(arr)<=1:
            # print(arr,'bottom')
            return 0, arr 

        arr = self.choose_pivot(arr) # now the first element is our pivot
        n = len(arr)
        # print(n)
        i=j=1 # i points to first element bigger than pivot, j points to first element unpartioned yet
        pivot = arr[0]
        while j<n:
            if arr[j]<=pivot:
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp
                j += 1
                i += 1
            else:
                j += 1
        # print(i)
        arr[:i-1] = arr[1:i]
        arr[i-1] = pivot
        # print(arr,'right after partition')
        left_arr = arr[:i-1]
        right_arr = arr[i:]
        left_comparisons, left_sorted = self.partition_by_pivot(left_arr)
        # print(left_arr)
        # print(right_arr)
        right_comparisons, right_sorted = self.partition_by_pivot(right_arr)
        self_comparisons = n-1
        arr[:i-1] = left_sorted
        arr[i:] = right_sorted
        return left_comparisons+right_comparisons+self_comparisons, arr

def compute(arr=None):
    qs = quickSort(choose_pivot='first')
    cnt, _ = qs.partition_by_pivot(arr=arr)
    return cnt




if __name__ == "__main__":
    # # test choose pivot
    # arr = np.array([0,10,2,5])
    # qs = quickSort(choose_pivot='first')
    # print(qs.choose_pivot(arr))
    # arr = np.array([0,10,2,5])
    # qs = quickSort(choose_pivot='last')
    # print(qs.choose_pivot(arr))
    # arr = [0,10,30,20,50,156,146,156]
    # qs = quickSort(choose_pivot='median')
    # print(qs.choose_pivot(arr))

    # # test partition by pivot
    # arr = [0,10,30,20,50,156,146,156,-10,290,10,10]
    # qs = quickSort(choose_pivot='first')
    # n_comparison, sorted_arr = qs.partition_by_pivot(arr)
    # print(n_comparison)
    # print(sorted_arr)

    # arr = [0,10,30,20,50,156,146,156,-10,290,10,10]
    # qs = quickSort(choose_pivot='last')
    # n_comparison, sorted_arr = qs.partition_by_pivot(arr)
    # print(n_comparison)
    # print(sorted_arr)

    # arr = [2, 20, 1, 15, 3, 11, 13, 6, 16, 10, 19, 5, 4, 9, 8, 14, 18, 17, 7, 12]
    # qs = quickSort(choose_pivot='median')
    # n_comparison, sorted_arr = qs.partition_by_pivot(arr)
    # print(n_comparison)
    # print(qs.comparisons_)
    # print(sorted_arr)

    # read in text file
    filename = sys.argv[1]
    print(filename)
    with open(filename) as f:
        intList = f.readlines()
    intList = [int(x.strip()) for x in intList]
    arr = np.array(intList)
    qs = quickSort(choose_pivot='median')
    st = time()
    n_comparison, sorted_arr = qs.partition_by_pivot(arr)
    print(n_comparison)
    print(qs.comparisons_)
    print(sorted_arr[-20:])
    ed = time()
    print('estimated computing time for %d-length array: %.3fs'%(len(arr), ed - st))

