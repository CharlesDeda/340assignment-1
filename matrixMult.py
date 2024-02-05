def matrixMult(n,m):
    result = [[0 for i in range(len(n))] for j in range(len(m))] #result must be leftRow rightCol
    for i in range(len(n)): #numRows n matrix
        for j in range(len(m[0])): #numCols m Matrix
            for k in range(len(m)): #numRows m matrix
                result[i][j] += n[i][k] * m[k][j] #result matrix
    return result

