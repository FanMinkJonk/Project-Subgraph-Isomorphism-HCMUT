# Adding necessary libraries
import os
import logging
from pandas import read_csv 
from scipy.sparse import coo_matrix

def getlogger():
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)                                                                                                                                                                                             
    return logger
# Assume that the file format is .mmio
# adj_mtx_file and inc_mtx_file are input files. Those files are respectively adjacent matrix and incident matrix.
# also assume that indexing is 1-based (MATLAB) not 0-based
def triangle(adj_mtx_file, inc_mtx_file):

    logger = getlogger()
    dataset_name = os.path.split(os.path.split(adj_mtx_file)[0])[1]
    logger.info('processing ' + dataset_name)

    # Figure out the shape of the adjacency matrix
    a = read_csv(adj_mtx_file, sep='\s+', header=None, nrows=1, dtype=int).values
    M1 = a[0,0]
    N1 = a[0,1]
    # Figure out the size of the incident matrix
    a = read_csv(inc_mtx_file, sep='\s+', header=None, nrows=1, dtype=int).values
    M2 = a[0,0]
    N2 = a[0,1]
    
    # Read the adjacency matrix
    y = read_csv(adj_mtx_file, sep='\s+', header=None, skiprows=1, dtype=int).values

    # Convert data to sparse matrix using the coo_matrix function in scipy.sparse
    A = coo_matrix(( y[:,2], (y[:,0]-1, y[:,1]-1)), shape=(M1,N1) )
    
    # Read the incident matrix
    y = read_csv(inc_mtx_file, sep='\s+', header=None, skiprows=1, dtype=int).values

    # Reshape the incident matrix
    B = coo_matrix( ( y[:,2], (y[:,0]-1, y[:,1]-1) ) , shape=(M2,N2) )

    # The final step is to count triangles
    logger.info('counting triangles')
    A = A + A.transpose()
    adjMtx = A.tocsr()
    incMtx = B.tocsr()
    C =  adjMtx * incMtx
    num_triangles = (C==2).nnz/3
    logger.info('number of triangles: ' + str(num_triangles))

    return (num_triangles)


triangle('#Input adj_mtx_file directory goes here#', "#Input inc_mtx_file directory goes here#")
########################################################
# GraphChallenge Benchmark
# Developer : Dr. Siddharth Samsi (ssamsi@mit.edu)
#
# MIT
########################################################
# (c) <2017> Massachusetts Institute of Technology
########################################################
