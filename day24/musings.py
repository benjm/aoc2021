# theorising - not .py but useful for bracket matching

A  0: Z = A + 4
B  1: Z = ( A + 4 ) * 26 + B + 10
C  2: Z = ( ( A + 4 ) * 26 + B + 10 ) * 26 + C + 12
D  3: Z = ( ( ( A + 4 ) * 26 + B + 10 ) * ( ( 25 * ( ( C + 6 == D ) == 0 ) ) + 1 ) ) + ( D + 14 ) * ( ( C + 6 == D ) == 0 )
E  4: Z = Z * 26 + E +  6
F  5: Z = Z * 26 + F + 16
G  6: Z = ( ( Z // 26 ) * ( ( 25 * ( ( F + 7 == G ) == 0 ) ) + 1 ) ) + ( G +  1 ) * ( ( F + 7 == G ) == 0 )
H  7: Z = Z * 26 + H +  7
I  8: Z = Z * 26 + I +  8
J  9: Z = ( ( Z // 26 ) * ( ( 25 * ( ( I + 3 == J ) == 0 ) ) + 1 ) ) + ( J + 11 ) * ( ( I + 3 == J ) == 0 )
K 10: Z = ( ( Z // 26 ) * ( ( 25 * ( ( ( ( Z % 26 ) -  9 ) == K ) == 0 ) ) + 1 ) ) + ( K +  8 ) * ( ( ( ( Z % 26 ) -  9 ) == K ) == 0 )
L 11: Z = ( ( Z // 26 ) * ( ( 25 * ( ( ( ( Z % 26 ) -  5 ) == L ) == 0 ) ) + 1 ) ) + ( L +  3 ) * ( ( ( ( Z % 26 ) -  5 ) == L ) == 0 )
M 12: Z = ( ( Z // 26 ) * ( ( 25 * ( ( ( ( Z % 26 ) -  2 ) == M ) == 0 ) ) + 1 ) ) + ( M +  1 ) * ( ( ( ( Z % 26 ) -  2 ) == M ) == 0 )
N 13: Z = ( ( Z // 26 ) * ( ( 25 * ( ( ( ( Z % 26 ) -  7 ) == N ) == 0 ) ) + 1 ) ) + ( N +  8 ) * ( ( ( ( Z % 26 ) -  7 ) == N ) == 0 )


( ( A + 4 ) * 26 + B + 10 ) * 26 + C + 12

for Z to be 0 at the end (N), either:
	 ( Z // 26 ) * ( ( 25 * ( ( ( ( Z % 26 ) -  7 ) == N ) == 0 ) ) + 1 ) == -(8 + N)
	 # N is in the range 1..9
	 # ( Z // 26 ) * ( ( 25 * ( ( ( ( Z % 26 ) -  7 ) == N ) == 0 ) ) + 1 ) in range [-9 .. -17]
	 # rhs of multiplication is either 26 or 1
	 # lhs of == is either (Z // 26) * 26 or (Z // 26) and the former does not work out as it'll either be 0 or a multiple of 26, neither of which are in the result range
	 # lhs is Z // 26 and must be a negative multiple of 26 therefore
	 # Z % 26 == N + 7
	 # Z // 26 == - N - 8
	 # Z(M) is (-N-8)*26 + N + 7


# UGH ... really confused ... some good discussion here:
# https://www.reddit.com/r/adventofcode/comments/rnejv5/2021_day_24_solutions/

