

import random

nus = [1,2,3]
wn = []

plc = 100000
lc = random.choice(nus)
for x in range(0,plc):
     y = random.choice(nus)
     if y ==  lc:
          wn.append(y)
     else:
          pass

l = len(wn)

l2 = 0.1 * plc
wun = l2 * 30 * 5

ls = plc - l2

loss = ls * 30

print("Won players  = " + str(l) )


print("Won amount  = " +str(wun) )


print("Made amount  = " +  str(loss))


print("Profits  = Ksh  " + str(loss - wun ))


print("Win Rate " + str(l2 / plc * 100))
