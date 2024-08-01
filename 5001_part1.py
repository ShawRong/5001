from readfile import read_docs
from itertools import combinations
import csv

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection/union

#main part
bbc_path = 'bbc/'
dirs = ['business','entertainment','politics','sport','tech']
dirs = [bbc_path + d for d in dirs]
documents = read_docs(dirs)

similarity_pairs = []
for i, j in combinations(range(len(documents)), 2):
    sim = jaccard_similarity(documents[i].document, documents[j].document)
    if sim >=0.5:
        similarity_pairs.append((i, j, sim))

#output part
output_list = []
for pair in similarity_pairs:
    d1, d2, s = pair
    filename1, filename2 = documents[d1].name, documents[d2].name
    output_list.append([f"{filename1}_{d1}",f"{filename2}_{d2}",f"{s:.2f}"])
            
csv_filename = 'part1.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Row', 'Column', 'Similarity'])
    csvwriter.writerows(output_list)


    
