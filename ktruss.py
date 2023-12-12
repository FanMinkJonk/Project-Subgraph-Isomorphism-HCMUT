# Adding necessary libraries
import numpy as np
import scipy as sp
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix

###################################################
###################################################

# Defining StrArryRead function to read through test-case files
def StrArrayRead(filename):
    f=open(filename,'r')
    edgelist = []
    with open(filename, 'r') as f:
        for line in f:
            edgelist.append(list(map(int, line.split('\t'))))
    f.close()
    return np.asarray(edgelist)

###################################################
###################################################

# Setting rows to 0
def set_zero_rows(sparray, rowNum):
    for row in rowNum:
        sparray.data[sparray.indptr[row]:sparray.indptr[row+1]]=0

###################################################
###################################################

# This function is used to write the result to a separate output file
def StrArrayWrite(nparray, filename):
    f=open(filename,"w")
    rows, cols = np.where(nparray == 1)
    incidence_list = list(zip(rows, cols, np.ones(len(rows), dtype=int)))
    data = [str(row[0]+1) + '\t\t' + str(row[1]+1) + '\t\t' + str(row[2]) + '\n' for row in incidence_list]
    f.write('Edges\t\tVertices\tTrue Variable\n')
    f.write(''.join(data))
    f.close()

###################################################
###################################################

def ktruss (inc_mat_file, inc_output_file,k):
    
    # Read the input file then save it in ii
    ii=StrArrayRead(inc_mat_file)
    
    # Convert the ii to a sparse matrix using csr_matrix available in scipy.sparse lib
    E=csr_matrix(( ii[:,2], (ii[:,0]-1, ii[:,1]-1)), shape=(max(ii[:,0]),max(ii[:,1])))
    
    tmp=np.transpose(E)*E
    sizeX,sizeY=np.shape(tmp)
    print( "Computing k-truss")
    tmp.setdiag(np.zeros(sizeX),k=0)
    tmp.eliminate_zeros()
    R= E * tmp
    s=lil_matrix(((R==2).astype(int)).sum(axis=1))
    xc= (s >=k-2).astype(int)
    
    while xc.sum() != np.unique(sp.sparse.find(E)[0]).shape:
        x=sp.sparse.find(xc==0)[0]
        set_zero_rows(E, x)
        E=(E>0).astype(int)
        E.eliminate_zeros()
        tmp=np.transpose(E)*E
        (tmp).setdiag(np.zeros(np.shape(tmp)[0]),k=0)
        tmp.eliminate_zeros()
        R=E*tmp
        s=csr_matrix(((R==2).astype(int)).sum(axis=1))
        xc= (s >=k-2).astype(int)

    # Start writing the result to inc_output_file    
    nparray=E.toarray()
    StrArrayWrite(nparray, inc_output_file)
    print( "Done! Check output files for result")
    return E

ktruss('#Input file directory goes here#','#Output file directory goes here#', 'the wanted value k (INT)')

###################################################
# Graph Challenge benchmark
# Developer: Dr. Vijay Gadepally (vijayg@mit.edu)
# MIT
###################################################
# (c) <2015> Vijay Gadepally
###################################################
