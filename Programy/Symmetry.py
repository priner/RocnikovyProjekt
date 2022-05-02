import itertools

# TODO treba checkovat xor ci je nula, a grupuj konektory

all_vertex_mapping = list(map(lambda pm: {str(i+1):pm[i] for i in range(4)}, itertools.permutations('1234')))

def map_point(vertex_mapping, original_array):
    new_array = []

    for point in original_array:
        newPoint = ""
        for v in point:
            newPoint += vertex_mapping[v]

        new_array.append(''.join(sorted(newPoint)))

    return tuple(new_array)

def normalize(original_array):
    return min(map(lambda vm: map_point(vm, original_array), all_vertex_mapping))

def all_colorings(length):
    return list(sorted(set(map(normalize, itertools.product(['1','2','3','4','12','13','14','23','24','34'], repeat=length)))))
