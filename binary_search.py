# Create a binary search that returns index of target (MUST BE SORTED)

test_list = [1,9,14,21,56,100,200,345,346,500,900,9000]


def binary_search(list, target, low=None, high=None):
    # Step 1
    if low == None: # If first iteration
        low = 0 # Lowest index will be 0 at any given time
    if high == None:
        high = len(list)- 1 # Highest index will be len of list, -1 since starts at 0
    
    # If not in list
    if high < low:
        return -1
        
    # Step 2    
    midpoint = (low + high) // 2 # To find midpoint, take average of lowest and highest index
    
    # Step 3
    if list[midpoint] == target: # If list at mid index is target, return that index
        return midpoint        
    elif target < list[midpoint]: # Else if target is less than value at mid index, 
        return binary_search(list, target, low, midpoint-1) # Use recursion, using range from current low to 1 less than mid.
        # This recursion starts at step 2
    else:
        # target > list[midpoint]
        return binary_search(list, target, midpoint+1, high)

print(binary_search(test_list, 9000))