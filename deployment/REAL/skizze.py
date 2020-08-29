
def f(x):
    def g(y):
        return y #+ x + 3
    return g

nf1 = f(1)
nf2 = f(3)


print(nf1(1))
print(nf2(2))



import sys
print("\n".join(sys.path))
sys.path.append('/Users/patrickrs/Documents/Github/sentencetransformers/sentencetransformers')
import SentenceTransformer