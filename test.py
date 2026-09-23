test_dict = {1: [10,100,1000], 2: [2, 200, 2000], 3: [3, 30, 300]}

count = 0
for value in test_dict.values():
    for i in value:
        print(i)
