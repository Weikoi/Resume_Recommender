
import matplotlib.pyplot as plt

import pickle as pk

df = pk.load(file=open("./df.pkl", "rb"))

df.hist(["predict"])
plt.show()