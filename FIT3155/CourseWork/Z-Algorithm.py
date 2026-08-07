# Given the string Str[0...i..L..N]

# We will output Z[0..... i.....N] -> where Z[i] is the length of the longest sub string starting from Str[i...L-1]
# that matches its prefix (i.e str[i..i+Z-1] = str[1...Zi])

''' 
So For S = 'aabcaabxaay' , Len = N
Z will be    Z = [N,   1,   0, 0,   3,       1,   0, 0,   2,      1,  0]
Which means, Z = [11, S[0], 0, 0, S[0,1,2], S[0], 0, 0, S[0,1], S[1], 0] is being counted  
Therfore the Z-box is Z[1] = [2..2], Z[2] = Undefined, Z[4] = [5..7] Formally this is written as Zi-box = [i..L-1] 
For each Z-Box we introduce a value r that is the index of the furtherst letter we have seen. e.g r1 = 2, r4 = 6 
Meanwhile a value l is the start index of the corrosponding Z-Boxes
 l1 = 1, l4 = 4,  l7 = 4,  l9 = 8  ... If we have multiple Z boxes ending at the same place l can be either index defined
 r = start_index + length (defined by Z) 
'''

def z_algorithm(s: str) -> list[int]:
    """
    Compute the Z-array for a string.

    z[i] is the length of the longest substring starting at i
    that matches the prefix of s.
    """

    n = len(s)
    if n == 0:
        return []
    # initiliase Z array
    z = [0] * n
    # intiliase Z box Variables
    left = 0
    right = 0

    # Driving Loop, starting from Index 1
    for i in range(1, n):  
        if i <= right: # This checks if the current index i is inside the Z-box. left --- i---- right
            z[i] = min(right - i + 1, z[i - left]) # copy previous Z-Value
            
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1

        if i + z[i] - 1 > right:
            left = i
            right = i + z[i] - 1

    z[0] = n
    return z


if __name__ == "__main__":
    sample = "aabxaayaab"
    print("String:", sample)
    print("Z-array:", z_algorithm(sample))

    