from common.basic_operation import *
from qr_decompose import *

def eigen_quodratic(tbl_name, q, r, dim, conn):
    """
    apply QR factorization until some maximum iteration reached
    """
    create_vector_or_matrix(q, conn)
    create_vector_or_matrix(r, conn)
    for k in range(51):
        qr_decompose(tbl_name, q, r, dim, conn)
        matrix_multiply_matrix_overwrite(r, q, tbl_name, conn)
    matrix_multiply_matrix_overwrite(q, r, tbl_name, conn)        
    assign_to(tbl_name, r, conn)