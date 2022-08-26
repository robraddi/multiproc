'''
Author: Rob Raddi
Edits on: April 4th, 2022
'''

import multiprocessing as mp
from multiprocessing import Manager
import numpy as np
from platform import python_version

def multiprocess(*args, **kwargs):
    """Decorator method for multiprocessing functions.
    Please refer to https://docs.python.org/3/library/multiprocessing.html#multiprocessing.sharedctypes.multiprocessing.Manager
    for manager types.

    https://docs.python.org/3.8/library/multiprocessing.html#contexts-and-start-methods
    # FIXME: Python >= 3.8
    #process = p.Process(target=function, args=(iter,), ctx=mp.get_context(method='fork'))
    """

    pyVersion = python_version()
    pyVersion = float(".".join(pyVersion.split(".")[:2]))

    def wrapper(function):
        n = len(kwargs['iterable'])
        print("Number of CPUs: %s"%(mp.cpu_count()))
        p = mp.Pool(processes=n)
        print(f"Number of processes: {n}")
        jobs = []
        mp.freeze_support()
        for iter in kwargs['iterable']:
            if pyVersion >= 3.8:
                process = p.Process(target=function, args=(iter,), ctx=mp.get_context(method='fork'))
            else:
                process = p.Process(target=function, args=(iter,))
            jobs.append(process)
            jobs[-1].start()
            active_processors = [jobs[i].is_alive() for i in range(len(jobs))]
            if (len(active_processors) == mp.cpu_count()-1) and all(active_processors) == True:
                while all(active_processors) == True:
                    active_processors = [jobs[i].is_alive() for i in range(len(jobs))]
                inactive = int(np.where(np.array(active_processors) == False)[0])
                jobs[inactive].terminate()
                jobs.remove(jobs[inactive])
        for job in jobs:
            job.join()
        p.close()
    return wrapper



if __name__ == "__main__":
    mp.freeze_support()
    multiprocess()




