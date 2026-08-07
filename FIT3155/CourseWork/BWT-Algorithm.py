''' Given a Suffix Array (SA) of a string append $ S[n] = $ and then 
we sort it, For example the string "googol$"
starts as 
          1: g o o g o l $
          2: o o g o l $
          3: o g o l $
          4: g o l $
          5: o l %
          6: l $
          7: $
Is then storted lexicographically -> 
          7: $
          4: g o l $
          1: g o o g o l $
          6: l $
          3: o g o l $
          5: o l %
          2: o o g o l $

If we note the would be positions of the letters after the $, we can find the last character that would have been:
                         # <- This last row is what we care about 
   m =    7: $ G O O G O L
          4: g o l $ G O O
          1: g o o g o l $
          6: l $ G O O G O
          3: o g o l $ G O
          5: o l % G O O G
          2: o o g o l $ G
          # <- This row is SA, suffix array

This gives the result of the algorithm, that is S = googol$ -> BWT(S) = lo$oogg

Another apporach is to say, subtracting one from the suffix array SA(that stores indexes of sorted suffixes of S) gives you the last column value
e.g for the first row we take SA[7-1] = S[6] = L
                              SA[4-1] = S[3] = O  e.t.c
Note in 1 based indexing,     SA[1-1] = S[0] = S[n = 7] = $



Further we want to iteratively recreate our Original String from our BWT(S)
To do this we firstly sort the string, so for "lo$oogg" -> "$gglooo"
From this we can construct the First column of M, Notice that the row containing $ leads to l -> therfore 'l' is the last char in String,
follow 'L' from First row ... Last row we get 'o' (at row 6). However now there are 3 'o's to choose from. See below;
Notice the grouping of 'g' and 'o', When we backsearch for our string we notice there are multiple 'o's and 'g's to pick.

To do this we find the position by F[pos] = Rank(L[i] + num_of_occurances(L[i], L[1...i]))
let L[i] = x, rank(x) = the position where x first appears in L[1..i)                 ^ not including index i
To use this we need to construct;
rank matrix = [Symbol, $, g, l, o]           From:   Symbol $, g, l, o
              [Rank,   1, 2, 4, 5]                    cnt   1, 2, 1, 3
Formally the Rank of each symbol is intiated to the num Of occurances, the order of symbol is lexigrapical.
Then the Rank is calculated as the prev_value + cur_value (iteratively till the end).


With all of this we can iterate over F and L to reconstruct:
F = [$, g, g, l, o, o, o]        We see $ -> so 'l$',  rank(l) = 4 + 0, so F[4] = o so 'ol$', rank(o) = 5 + 1, so F[6] = 'gol$', rank(g) = 2 + 0 = F[2] so 'ogol$' e.tc
L = [l, o, $, o, o, g, g]  




Using BWT for pattern matching:
initally: sp = 1, ep = n | The driving formula is as follows:
start pointer, sp = rank(pat[i] + nOccur(pat[i], L[1..sp))) <-- exclusive
End pointer,   ep = rank(pat[i] + nOccur(pat[i], L[1...ep])) - 1 <-- Inclusive 

So for pat[1...m] = 'go'
       txt[1...n] = 'googol$'
       pos = 1 2 3 4 5 6 7
We L[1..n] = l o $ o o g g // BWT of txt
and     SA = 7 4 1 6 3 5 2 //suffix array index

We look over like so:

            l   <- sp
            o
            $
            o
            o
            g
            g <- ep

            until the pointers point between two points, taking the i valve of these, taking the SA[i] value in the pattern 
            gives what letters they should be for example SA[4] = 6 means txt[6] = 'g'
            so we look up based on the range [sp..ep] .... SA[sp] + SA[ep] 
'''

input_text = 'banana$'
bwt_arr = []
suffix_arr = []

def compute_suffix_array(input_text, len_text):
    # Array of structures to store rotations and their indexes
    suff = [(i, input_text[i:]) for i in range(len_text)]

    # Sorts rotations using comparison function defined above
    suff.sort(key=lambda x: x[1])

    # Stores the indexes of sorted rotations
    suffix_arr = [i for i, _ in suff]

    # Returns the computed suffix array
    return suffix_arr

def find_last_char(input_text, suffix_arr, n):
    # Iterates over the suffix array to
    # find the last char of each cyclic rotation
    bwt_arr = ""
    for i in range(n):
        # Computes the last char which is given by 
        # input_text[(suffix_arr[i] + n - 1) % n]
        j = suffix_arr[i] - 1
        if j < 0:
            j = j + n
        bwt_arr += input_text[j]

    # Returns the computed Burrows-Wheeler Transform
    return bwt_arr

SA = compute_suffix_array(input_text, len(input_text))
print(SA)

bwt_arr = find_last_char(input_text, SA, len(input_text))
print(bwt_arr)