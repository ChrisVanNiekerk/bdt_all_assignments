def mapping(data):

    map_list=[]

    for label in data:

        if len(data[label]) == 1:

            for word in data[label][0].split():

                map_list.append((word,label))

        else:

            for word in data[label]:

                map_list.append((word,label))

    return map_list

def reduce(map_list):

    reduce_dict = {}

    for pair in map_list:

        if pair[0] not in reduce_dict.keys():

            reduce_dict[pair[0]] = [pair[1]]

        if pair[1] in reduce_dict[pair[0]]:

            continue

        else:
            reduce_dict[pair[0]].append(pair[1])

    return reduce_dict

data = {'D1': ['the cat sat on the mat'],
       'D2': ['the dog sat on the log']}

map_list = mapping(data)
reduce_result = reduce(map_list)

print(reduce_result)
