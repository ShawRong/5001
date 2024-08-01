#part2
from sympy import isprime
import numpy as np
from readfile import read_docs
from itertools import combinations
import csv

# hash function part
def next_prime(n):
    prime = n + 1
    while not isprime(prime):
        prime += 1
    return prime

def hash_function_generator(a, b, c):
    def hash_function(r):
        return (a * r + b) % c
    return hash_function

def generate_hash_function_list(max_val, function_num = 50):
    a_list = np.random.randint(1, max_val, size= function_num) #a cant be zero
    b_list = np.random.randint(1, max_val, size= function_num)
    c = next_prime(max_val)
    hash_function_list = []
    for i in range(0, function_num):
        a = a_list[i]
        b = b_list[i]
        c = c
        hash_function_list.append(hash_function_generator(a, b, c))
    return hash_function_list


#signature part
def generate_signature_matrix(documents, hash_func_list):
    hash_function_num = len(hash_func_list)
    documents_num = len(documents)
    signature_matrix = np.full((hash_function_num, documents_num), np.inf)
    
    for doc_idx in range(documents_num):
        doc = documents[doc_idx]
        for r in doc:
            for i in range(hash_function_num):
                hash_function = hash_func_list[i]
                hash_value = hash_function(r)
                if hash_value < signature_matrix[i, doc_idx]:
                    signature_matrix[i, doc_idx] = hash_value
    return signature_matrix


#main part
bbc_path = 'bbc/'
dirs = ['business','entertainment','politics','sport','tech']
dirs = [bbc_path + d for d in dirs]
documents_with_name = read_docs(dirs)

documents = [doc.document for doc in documents_with_name]
max_val = max(max(doc) for doc in documents)
hash_func_list = generate_hash_function_list(max_val, 50)

sig_matrix = generate_signature_matrix(documents, hash_func_list)

k, n = sig_matrix.shape
similarity_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if i != j:
            similarity_matrix[i, j] = np.sum(sig_matrix[:, i] == sig_matrix[:,j]) / k
        else:
            similarity_matrix[i, j] = 1 # it and itself


similarity_pairs = []
for i, j in combinations(range(n), 2):
    sim = similarity_matrix[i, j]
    if sim >=0.5:
        similarity_pairs.append((i, j, sim))

#output part
documents = documents_with_name
output_list = []
for pair in similarity_pairs:
    d1, d2, s = pair
    filename1, filename2 = documents[d1].name, documents[d2].name
    output_list.append([f"{filename1}_{d1}",f"{filename2}_{d2}",f"{s:.2f}"])
            
csv_filename = 'part2.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Row', 'Column', 'Similarity'])
    csvwriter.writerows(output_list)
        

    
