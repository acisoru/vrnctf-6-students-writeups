from Crypto.Util.number import bytes_to_long
import json
with open("./flag.txt", "rb") as f:
    FLAG = f.read().strip()

with open("./curve.json") as f:
    curve_params = json.loads(f.read())


def public_key():
	d = bytes_to_long(FLAG)
	return G * d

p = int(curve_params["field"]["p"])
a = int(curve_params["a"])
b = int(curve_params["b"])
E = EllipticCurve(GF(p), [a, b])

G = E.gens()[0]
Q = public_key()
print(f"p = {p}")
print(f"Q = {Q.xy()}")
print(f"G = {G.xy()}")
