import random

def shuffled(not_shuffled):
    ''' returns a shuffled list'''

    new_list = not_shuffled.copy()
    random.shuffle(new_list)

    return new_list


test_list = [1, 2, 3, 4, 5]
# print(shuffled(test_list))

# for item in shuffled(test_list):
#     print(item)

for item in shuffled(test_list):
    test_list.remove(item)
    print(f"{item} removed")
