def ArraySumOdd(vals):
    sumsum = 0
    # loop through the list
    for listval in vals:
        test = listval % 2
        # check for non-zero remainders to find odd numbers
        if test != 0:
            # sum up the sum and stuff
            sumsum += listval
    return sumsum

def MatrixProductLargerThan(A, val):
    larger = 1
    # loop through the matrix values
    for row in A:
        for col in row:
            # product of matrix values higher than given value
            if col > val:
                larger *= col
    return larger

def polyval(x, coeffs):
    pval = 0
    for coeff in range(len(coeffs)):
        # loop through each coeff, and add product with x to the power of coeff position
        pval += ((x ** coeff) * coeffs[coeff])
    return pval

def location_of_largest(amatrix):
    most_a = 0
    most_b = 0
    largestval = 0
    # loop through all matrix values using index method
    for a in range(len(amatrix)):
        for b in range(len(amatrix[a])):
            # check if current value is higher than previous highest value
            if largestval < abs(amatrix[a][b]):
                largestval = abs(amatrix[a][b])
                # store the value and index positions for true condition
                most_a = a
                most_b = b
    return most_a, most_b



def main():
    # define the variables needed to test the required functions
    myvals = [-1,5,2,-3,5,5,3,-5,2,5,3,3,1,5]
    mymatrix1 = [[1, 3.7, -7, 4],
                [-8, 9, 2, -1.8],
                [-12, 7.9, 3.2, 13]
                ]
    mymatrix2 = [[1, 3.7, -7],
                [-8, 9, -1.8],
                [7.9, 3.2, -11],
                [4.3, -0.32, 4]
                ]

    p1 = [3,   1, -2, -4]
    p2 = [2, 1.4,  1, -1, 2]

    x1 = 1.3
    x2 = -2.4

    # part a)
    ans1 = ArraySumOdd(myvals)
    ans2 = ArraySumOdd(p1)
    print('part a)  ', ans1, ans2)
    print()  # print a blank line

    # part b)
    ans1 = MatrixProductLargerThan(mymatrix1, x1)
    ans2 = MatrixProductLargerThan(mymatrix2, -1.5)
    print('part b)  ', ans1, ans2)
    print()  # print a blank line

    # part c)
    poly = polyval(x1, p1)
    print('part c)  Polynomial value for (x1= {:.2f}) = {:.1f}'.format(x1, poly))
    poly = polyval(x2, p2)
    print('part c)  Polynomial value for (x2= {:.2f}) = {:.1f}'.format(x2, poly))
    print()  # print a blank line

    # part d)
    row, col = location_of_largest(mymatrix1)
    val = mymatrix1[row][col]
    print('part d) ', val, row, col)
    row, col = location_of_largest(mymatrix2)
    val = mymatrix2[row][col]
    print('part d) ', val, row, col)


main()
