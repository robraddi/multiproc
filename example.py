import multiproc as mproc
import numpy as np

"""
In this example, we will create two instances of calling on multiproc.
Note that when two separate instances of multiproc are given to the interpreter
at the same time (e.g., python exmaple.py).
Note that multiprocessing will return results as they finish and are not ordered
unless enforced.


1. A simple example using `print`
  - iterable must be a list or tuple, and cannot be a class oject like `range()`


2. An example that stores information (`results`) during multiprocessing
  - it is wise to store the iter (`index`) if your results require ordering


"""


def some_function(x):
    return np.exp(-x**2)*np.cos(x)



if __name__ == "__main__":
    mproc.freeze_support()

    # 1.
    @mproc.multiprocess(iterable=list(range(10)))
    def simple_print(i):
        print(i)

    print("\n\n") ######################################

    # 2.
    N = 10
    x = np.stack([
        np.array(list(range(N))),
        np.array(list(range(N))), #np.sort(np.random.random((N)))
        ], axis=1)

    with mproc.Manager() as manager:
        results = manager.list()
        list_of_dict = [{"index":int(i), "value":v} for i,v in x]
        @mproc.multiprocess(iterable=list_of_dict)
        def function(list_of_dict):
            index, f = list_of_dict["index"], some_function(float(list_of_dict["value"]))
            results.append([index,f])

        print(results)



