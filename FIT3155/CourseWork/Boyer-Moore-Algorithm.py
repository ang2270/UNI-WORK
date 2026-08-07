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


