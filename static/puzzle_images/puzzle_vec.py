import pypuzzle
puzzle = pypuzzle.Puzzle()
vec1 = puzzle.get_cvec_from_file('elder_copy.jpg')
vec2 = puzzle.get_cvec_from_file('elder_copy_2.jpg')

for i in range(len(vec1)/50 + 1):
    print ''.join(['%3d' % j for j in vec1[i*50: (i+1)*50]])
    print ''.join(['%3d' % j for j in vec2[i*50: (i+1)*50]])
    raw_input()
