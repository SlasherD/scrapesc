######### Cyan #########
### Basic timekeeper ###

from time import perf_counter as _time


def timekeeper(func):
    def wrapper():
        start = _time()
        func()
        end = _time()
        timer = 1000 * (end-start) # in milliseconds
        print(f'{"-"*11} Execution time: {timer:.0f} ms {"-"*11}')
        print(f'{"Finished executing block":^50}',
              f'{"-+-"*10:^50}', sep='\n', end='\n\n')
    return wrapper