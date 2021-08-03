def partition(array, begin, end):
    pivot = begin

    for num in range(begin + 1, end + 1):

        if array[num] >= array[begin]:
            pivot += 1
            array[num], array[pivot] = array[pivot], array[num]

    array[pivot], array[begin] = array[begin], array[pivot]
    return pivot


def quicksort(array, begin = 0, end = None):
    print(array)

    if end is None:
        end = len(array) - 1

    if begin >= end:
        return

    pivot = partition(array, begin, end)
    quicksort(array, begin, pivot-1)
    quicksort(array, pivot+1, end)

def insertion_sort(array, end=None):
    if end is None:
        end = len(array) - 1

    if end >= 1:
        insertion_sort(array, end - 1)
        number = array[end]
        print("Number:", number)
        prev_index = end - 1

        while prev_index >= 0 and array[prev_index][0] < number[0]:
            array[prev_index + 1] = array[prev_index]
            prev_index -= 1

        array[prev_index + 1] = number
        print(array, end, number, prev_index)
