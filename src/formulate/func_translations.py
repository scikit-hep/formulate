
#maybe use num

def root_length(array):
    import awkward as ak
    while array.layout.purelist_depth > 2:
        array = ak.flatten(array, axis=-1)
    return ak.count(array, axis=-1)


def root_sum(array):
    import awkward as ak
    while array.layout.purelist_depth > 2:
        array = ak.flatten(array, axis=-1)
    return ak.sum(array, axis=-1)


def root_min(array):
    import awkward as ak
    while array.layout.purelist_depth >= 2:
        array = ak.min(array, axis=-1)
    return ak.fill_none(array, 0)



def root_max(array):
    import awkward as ak
    while array.layout.purelist_depth >= 2:
        array = ak.max(array, axis=-1)
    return ak.fill_none(array, 0)


def root_min_if(array, condition):
    import awkward as ak
    array = array[condition != 0]
    return ak.fill_none(ak.min(array,axis=1),0)

def root_max_if(array, condition):
    import awkward as ak
    array = array[condition != 0]
    return ak.fill_none(ak.max(array,axis=1),0)