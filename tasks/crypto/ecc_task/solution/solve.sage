import ast
from Crypto.Util.number import long_to_bytes, inverse

p = 473339786979736045038406156085680192186465257949
Q = (267237587507047813630925154790345406982309922130, 157304695964268140982887631761365100533367068675)
G = (61111808781876303339708122795582074063180237485, 130812416853304375633986978222930019708479363865)

def pohlig_hellman(G, Q):
    order = G.order()
    divs = list(factor(order))
    print(divs)
    factors = [elem[0] ^ elem[1] for elem in divs]
    dlogs = []
    for fac in factors:
        print(f"working with factor {fac}")
        _G = G * (order // fac)
        _Q = Q * (order // fac)
        dlogs.append(discrete_log(_Q, _G, operation="+"))
    return crt(dlogs, factors)

gx, gy = G
qx, qy = Q

a = ((gy ** 2 - gx ** 3 - qy ** 2 + qx ** 3) * inverse(gx-qx, p)) % p
b = (gy ** 2 - gx ** 3 - a * gx) % p
assert (gx ** 3 + a * gx + b) % p == gy ** 2 % p
assert (qx ** 3 + a * qx + b) % p == qy ** 2 % p

E = EllipticCurve(GF(p), [a, b])
G = E(gx, gy)
Q = E(qx, qy)

print(hex(int(a)))
print(hex(int(b)))
print(factor(E.order()))
print(long_to_bytes(int(pohlig_hellman(G, Q))))
