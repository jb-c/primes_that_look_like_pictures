import math

class BaseNumber:
    '''
    A Wrapper class for the base number we want to modify
    '''
    def __init__(self,f_path):
        with open(f_path) as f:
            base_number_list = f.read().split('\n')

        self.string = ''.join(base_number_list)
        self.int = int(self.string)

        self.width = len(base_number_list[0])
        self.height = len(base_number_list)
        self.len = len(self.string)

    def print(self):
        '''
        Prints the base number row by row
        '''
        for i in range(math.ceil(self.len / self.width)):
            print(self.string[i*self.width:(i+1)*self.width])


base_number = BaseNumber('data/base_number.txt')