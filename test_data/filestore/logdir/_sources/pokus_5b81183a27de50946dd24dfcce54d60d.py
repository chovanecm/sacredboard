from sacred import Experiment

ex = Experiment("Pokus")

@ex.config
def config():
    depth = 5
    length=20
    return_info=False



def add_info(parent, depth, length):
    if depth == 0:
        return
    for i in range(length):
        parent["pos %d" % i] = "value %d" % i
    parent["child1 %d" % depth] = {}
    #parent["child2 %d" % depth] = {}
    add_info(parent["child1 %d" % depth], depth-1, length)
    #add_info(parent["child2 %d" % depth], depth-1, length)
    

@ex.automain
def my_main(_run, depth, length, return_info):
    add_info(_run.info, depth, length)
    if return_info:
        return _run.info

