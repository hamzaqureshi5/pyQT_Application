import sys
import shelve as sh
import pandas as pd
#print(sys.platform)
#import sys
#print ("Number of arguments:", len(sys.argv), "arguments")
#print ("Argument List:", str(sys.argv))
#$ python test.py arg1 arg2 arg3
#Number of arguments: 4 arguments.
#Argument List: ['test.py', 'arg1', 'arg2', 'arg3']

#for line in sys.stdin:
#    if 'Exit' == line.rstrip():
#        break
#    print(f'Processing Message from sys.stdin *****{line}*****')
#print("Done")


def input_file_validation(data):
     temp=([(c, data[c].dtype.kind in 'iufcb') for c in data.columns])
     temp1=[True for i in temp if i is True]
     print(temp1)
     result=False
     for i in temp1:
          if i is False:
               result= False
          else:
               result= True
          print(result)
     return result

def show_input_files():
     path='C:/Users/hamza.qureshi/Desktop/STC_APP/improvements/dataGen-v18-VS-CODE/Input Files/input.csv'
     data = pd.DataFrame()
     match path:
          case ""|" ":
               pass
          case _:
               data=pd.read_csv(path)
               print(input_file_validation(data))
#               print([(c, data[c].dtype.kind in 'iufcb') for c in data.columns])

                

#show_input_files()

def decorator_with_arguments(function):
     def wrapper_accepting_arguments(arg1, arg2):
          print("My arguments are: {0}, {1}".format(arg1,arg2))
          function(arg1, arg2)
     return wrapper_accepting_arguments


@decorator_with_arguments
def cities(city_one, city_two):
    print("Cities I love are {0} and {1}".format(city_one, city_two))

cities("Nairobi", "Helsinki")

import time

def measure_execution_time(func):
     def wrapper(*args, **kwargs):
          start_time = time.time()
          result = func(*args, **kwargs)
          end_time = time.time()
          execution_time = end_time - start_time
          print(f"Function '{func.__name__}' took {execution_time:.100f} seconds to execute.")
          print(f"Function '{func.__name__}' took {execution_time*1000000} microseconds to execute.")
          return result
     return wrapper

@measure_execution_time
def my_function():
#     for i in range(0,5):
         pass

my_function()



def simple_decorator(own_function):
     def internal_wrapper(*args, **kwargs):
          print('"{}" was called with the following arguments'.format(own_function.__name__))
          print('\t{}\n\t{}\n'.format(args, kwargs))
          own_function(*args, **kwargs)
          print('Decorator is still operating')
     return internal_wrapper


@simple_decorator
def combiner(*args, **kwargs):
     print("\tHello from the decorated function; received arguments:", args, kwargs)
     
combiner('a', 'b', exec='yes')


def warehouse_decorator(material):
     def wrapper(our_function):
          def internal_wrapper(*args):
               print('Wrapping items from {} with {}'.format(our_function.__name__, material))
               our_function(*args)
               print()
          return internal_wrapper
     return wrapper


@warehouse_decorator('kraft')
def pack_books(*args):
     print("We'll pack books:", args)


#pack_books('Alice in Wonderland', 'Winnie the Pooh')
import datetime


def timestamp_decorator(func):
    def wrapper(*args, **kwargs):
        now = datetime.datetime.now()
        print("Timestamp: {}".format(now))
        return func(*args, **kwargs)
    return wrapper

def timestamp_decorator1(func):
     def wrapper(*args,**kwargs):
          now=datetime.datetime.now()
          print("Time is {}".format(now))
          return func(*args,**kwargs)
     return wrapper
          

@timestamp_decorator1
def add_numbers(x, y):
    return x + y

#@timestamp_decorator
def multiply_numbers(x, y):
    return x * y

print(add_numbers(10, 20))
#print(multiply_numbers(10, 20))


import datetime
def decorators(func):
    def wrapper(*args,**kwargs):
        now=datetime.datetime.now()
        print("time is {}".format(now))
        return func(*args,**kwargs)
    return wrapper

@decorators
def add(x,y):
    return x+y

@decorators
def dot(x,y):
    return x*y

#add(5,3)

# import pickle

# my_list = [1, 2, 3]
# my_dict = {"name": "John", "age": 30}

# with open("my_data.pkl", "wb") as f:
#     pickle.dump(my_list, f)
#     pickle.dump(my_dict, f)

# with open("my_data.pkl", "rb") as f:
#     my_list_unpickled = pickle.load(f)
#     my_dict_unpickled = pickle.load(f)

# print(my_list_unpickled)
# print(my_dict_unpickled)
# print("AAAAAAAAAAAAAAAAAAAA")
# print(my_list)
# print(my_dict)

# fp=sh.open("shelve/file")
# fp.setdefault("AAA")

# print(fp.popitem())






import secrets

KID=135
conv_hex=(hex(135))
bin_hex=bin(1)

print(str(format( int(KID) , '016b')))
# print(str(conv_hex))
# print(secrets.token_hex(32).upper())
# print(len("65655a551f0114301254d9a77bf1fc06aae9725645c22bfdb49c263972effb78"))
import hashlib
import binascii
def derive_key_from_id(id_str):
    # Convert the ID string to bytes using UTF-8 encoding
    id_bytes = id_str.encode('utf-8')
    print("ID",id_bytes)

    # Calculate the SHA-256 hash of the ID bytes
    sha256_hash = hashlib.sha256(id_bytes,usedforsecurity=True).digest()
    hex_key = binascii.hexlify(sha256_hash)
    derived_key = hex_key.decode()
#    derived_key = sha256_hash[:]

    return derived_key,len(derived_key)

# Example usage:
id_str = "335"
key,t = derive_key_from_id(id_str)
print("Derived Key:", key,"Lenght : ",t)



from Crypto.Cipher import DES



def generate_operator_key1(op_id):
    # Convert the OP-ID to bytes (adjust the encoding based on your actual format)
    op_id_bytes = op_id.to_bytes(length=4, byteorder='big')
    print(op_id_bytes)

    # Example: Use SHA-256 to hash the OP-ID
    hashed_op_id = hashlib.sha224(op_id_bytes).digest()
    print(list(hashlib.algorithms_available))
    
    algos=list(hashlib.algorithms_available)


    # The Operator Key should be derived from the hashed OP-ID
    # You can further process the hashed_op_id to obtain the Operator Key
    # For example, take the first 16 bytes as the Operator Key
    operator_key = hashed_op_id[:]

    return operator_key

# Example usage with OP-ID 335
#op_id = 335
#operator_key = generate_operator_key(op_id)
##print(f"Operator Key: {operator_key.hex()}")


import hashlib

import hashlib

def generate_operator_key(op_id):
    # Convert the OP-ID to bytes (adjust the encoding based on your actual format)
    op_id_bytes = op_id.to_bytes(length=4, byteorder='big')

    # Create a dictionary to store the results
    result = {}

    # Loop through all available hash algorithms in hashlib
    for name in hashlib.algorithms_available:
        algorithm = hashlib.new(name)
        algorithm.update(op_id_bytes)
        hashed_op_id = algorithm.hexdigest()

        # The Operator Key should be derived from the hashed OP-ID
        # For example, take the first 16 characters of the hexadecimal representation as the Operator Key
        operator_key = hashed_op_id[:16]

        result[name] = operator_key

    return result


op_id = 335
operator_keys = generate_operator_key(op_id)
for name, key in operator_keys.items():
     print(f"{name}: {key}")
