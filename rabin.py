#!/usr/bin/env python

import sys

def prime_mod_sqrt(a, p):
    """
    Square root modulo prime number
    Solve the equation
        x^2 = a mod p
    and return list of x solution
    http://en.wikipedia.org/wiki/Tonelli-Shanks_algorithm
    """
    a %= p
    # Simple case
    if a == 0:
        return [0]
    if p == 2:
        return [a]
    # Check solution existence on odd prime
    if legendre_symbol(a, p) != 1:
        return []
    # Simple case
    if p % 4 == 3:
        x = pow(a, (p + 1)/4, p)
        return [x, p-x]
    # Factor p-1 on the form q * 2^s (with Q odd)
    q, s = p - 1, 0
    while q % 2 == 0:
        s += 1
        q //= 2
    # Select a z which is a quadratic non resudue modulo p
    z = 1
    while legendre_symbol(z, p) != -1:
        z += 1
    c = pow(z, q, p)
    # Search for a solution
    x = pow(a, (q + 1)/2, p)
    t = pow(a, q, p)
    m = s
    while t != 1:
        # Find the lowest i such that t^(2^i) = 1
        i, e = 0, 2
        for i in xrange(1, m):
            if pow(t, e, p) == 1:
                break
            e *= 2
        # Update next value to iterate
        b = pow(c, 2**(m - i - 1), p)
        x = (x * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i
    return [x, p-x]

def legendre_symbol(a, p):
    """
    Legendre symbol
    Define if a is a quadratic residue modulo odd prime
    http://en.wikipedia.org/wiki/Legendre_symbol
    """
    ls = pow(a, (p - 1)/2, p)
    if ls == p - 1:
        return -1
    return ls
    
def int2text(n, padright=True) :
    bin_n = bin(n)[2:]
    if len(bin_n) % 8 != 0:
        if padright == True :
            bin_n = bin_n + "0" * ( 8 - len(bin_n) % 8)
        else :
            bin_n = "0" * ( 8 - len(bin_n) % 8) + bin_n
    l = [ bin_n[i:i+8] for i in range(0, len(bin_n), 8) ]
    return ''.join(map(lambda b: chr(int(b, 2)), l))

class Polynomial(list):
    """A polynomial whose coeffients, from highest power to lowest, are given by list."""
    def __init__(self, clist):
        self.coeffs = clist
    
    def __repr__(self):
        sign = {
            (True, True): '-',
            (True, False): '',
            (False, True): ' - ',
            (False, False): ' + '
        }
        
        poly = []
        
        for n, a in reversed(list(enumerate(reversed(self.coeffs)))):
            s=sign[not poly, a<0]
            a=abs(a)
            if a==1 and n !=0:
                a = ''
            f={0:'{}{}', 1: '{}{}x'}.get(n, '{}{}x^{}')
            if a != 0: poly.append(f.format(s,a,n))
        return ''.join(poly) or ''
        
def FormalDerivative(f):
    """Returns a Polynomial which is the formal derivative of the polynomial f"""
    dc = Polynomial([])
    l=len(coeffs)
    for i in range(l-1):
        dc.coeffs.append((l-i-1)*coeffs[i])
    return dc

def Evaluate(f, x):
    """Evaluate f(x)"""
    r=0
    n=len(f.coeffs)-1
    for i in range(n+1):
        r += f.coeffs[i]*(x**(n-i))
    return r

def ExtendedEuclideanAlgorithm(a,b,c):
    """Returns the least x, y such that ax + by = c."""
    revflag=False
    if b>a:
        a,b=b,a
        revflag=True
    r , q = [a,b,a%b] , int(a/b)
    s , t = [1,0,1] , [0,1,-q]
    if r[2]==0:
        if c%b == 0:
            if revflag == False: return 0,c/b
            return c/b, 0
        return False
    while r[2]>0:
        q=int(r[1]/r[2])
        r[0], r[1], r[2] = r[1], r[2], r[1]%r[2]
        s[0], s[1], s[2] = s[1], s[2], s[1]-s[2]*q
        t[0], t[1], t[2] = t[1], t[2], t[1]-t[2]*q
    if c%r[1] != 0:
        return False
    d=c/r[1]
    if revflag: 
        s,t = t,s
    return d*s[1],d*t[1]

def Hensel(f,p,k):
    """Returns solutions to f(x) mod p^k = 0. """
    if k < 1: return False
    if k == 1:
        '''
        r=[]
        for i in range(p):
            if Evaluate(f,i)%p == 0:
                r.append(i)
        return r
        '''
        mp = prime_mod_sqrt(p - f.coeffs[2], p)
        print "mp : ", mp
        return mp
    r = Hensel(f,p,k-1)
    df=FormalDerivative(f)
    rnew=[]
    for i,n in enumerate(r):
        dfr=Evaluate(df,n)
        fr=Evaluate(f,n)
        if dfr%p != 0:
            t=(-(ExtendedEuclideanAlgorithm(dfr, p, 1)[0])*int(fr/p**(k-1)))%p
            rnew.append(r[i]+t*p**(k-1))
        if dfr%p == 0:
            if fr % p**k == 0:
                for t in range(0,p):
                    rnew.append(r[i]+t*p**(k-1))                
    return rnew

N = 75404462446621433278932073418166377856783371695311741162660984000216286022717332034344886883228963555598915581623574177254937709767805818855313080010310907057693076782794571905025544034519430835894406844610021327070351428935856401291946497064114909504725588880164068827953784803548706132824333011073782801921L
	
c = 9560634911497745583378708911423730041871108408354273851105442823652482446584728244370275783778971812977745029111313416532500401836444585708475658254699672285618254670808419777671613020408027434193662041848593393740726639973784613890042844233861571190841541366812077582649290826487514627722655599040743377675L

p = 8683574289808398551680690596312519188712344019929990563696863014403818356652403139359303583094623893591695801854572600022831462919735839793929311522108161L

coeffs = [1, 0, N-c]
f = Polynomial(coeffs)
k = 2
print 'Using Hensel\'s Lemma to find solutions for: '
print f, ' mod ', p, '^' ,k,'= 0'
r = Hensel(f,p,k)
print 'Solutions:', map(lambda n: int2text(n, False), r)

