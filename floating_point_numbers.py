import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

import numpy as np

#Working with (1,5,8) i.e. 1 for sign, 5 for exponent, 8 for mantissa
#input all as list of binary numbers i.e. 10111011001101 -> floating([1], [0,1,1,1,0],[1,1,0,0,1,1,0,1])

def convert(num: float):
    sign = '1' if num<0 else '0'
    tmp = abs(num)
    k = 2**(-15)
    exp = -1
    
    while k<=num:
        k = 2*k
        exp+=1
        
    if exp==-1 or exp>31:
        raise ValueError()
        
    x = num/2**(exp-15)-1
    mantissa = ''
    for i in range(1,9):
        y = 2**(-i)
        if x-y>=0:
            x= x-y
            mantissa+='1'
        else:
            mantissa+='0'
    exp = bin(exp)[2:]
    exp = exp if len(exp)==5 else '0'*(5-len(exp))+exp
    tmp = floating()
    tmp.f_setter(sign+exp+mantissa)
    return tmp
    
    
class floating():
    def __init__(self):
	    self.sign = 0
	    self.exp = 0
	    self.mantissa = 0
        
    def f_setter(self, bin_num: str):
        self.sign  = bin_num[0]
        self.exp = bin_num[1:6]
        self.mantissa = bin_num[6:]
        
    def f_getter(self):
        print(f'Sign: {self.sign}\nExp: {self.exp}\nMantissa: {self.mantissa}\nCombined: {self.sign+self.exp+self.mantissa}')
        
    def value(self):
        s = self.svalue()
        e = self.evalue()
        m = self.mvalue()
        return s*e*m
        
    def svalue(self):
        return 1 if self.sign =='0' else -1
      
    def evalue(self):
        return 2**(int(self.exp, base=2))/2**(15)
        
    def mvalue(self):
        return 1+int(self.mantissa, base=2)/2**8
        
    def __add__(self, other):
        s = self.value()
        o = other.value()
        result = convert(s+o)
        return result.value()
    
    def __sub__(self, other): #returns self - other
        s = self.value()
        o = other.value()
        result = convert(s-o)
        return result.value()
        
    def __mul__(self, other):
        temp = floating()
        temp_sign = str(int(self.sign)^int(other.sign))
        temp_mantissa = (256+int(self.mantissa, base=2))*(256+int(other.mantissa, base=2))
        if temp_mantissa >= 1<<17:
            temp_exp = bin(int(self.exp, base=2)+int(other.exp, base=2)-14)[2:]
            temp_mantissa = bin(temp_mantissa)[3:11]
        else:
            temp_exp = bin(int(self.exp, base=2)+int(other.exp, base=2)-15)[2:]
            temp_mantissa = bin(temp_mantissa)[3:11]
        if len(temp_exp)> 5 or 'b' in temp_exp:
            raise ValueError #This is to make sure that the product doesn't exceed the number system given i.e. become a number that requires more than 14 bits to describe or be smaller than 2^-15
        temp.f_setter(temp_sign+ temp_exp+ temp_mantissa)
        return temp
        
        

    def __str__(self):
        return self.sign+self.exp+self.mantissa
    
def main():
    #The following section plots all possible values for the given number system
    '''
    f = floating()
    x = [i for i in range(16384)]
    y = []
    for i in range(16384):
        i = bin(i)[2:]
        if len(i) != 14:
            i = '0'*(14-len(i))+i
        f.f_setter(i)
        y.append(f.value())
    
    plt.plot(x,y)
    plt.show()
    
    
    inp = float(input("What number would you like to conver to a floating point number?: "))
    conv = convert(inp)
    print('Your converted number is: ', conv)
    print('The floating point value is: ', conv.value())
    '''
    f = floating()
    g = floating()
    f.f_setter('00101100011100')
    g.f_setter("00100100101001")
    print(f'f: {f.value()}\ng: {g.value()}')
    r = f*g
    print("Product: ",r.value(), '\nwhat', r.f_getter())
    r = f+g
    print("Sum: ", r)
    r = f-g
    print("Difference: ", r)
main()