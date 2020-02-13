#!/usr/bin/python
import random
data = random.randint(0, 1000000);
f=  open(".code", "wb")
f.write('%d' % data)
f.close()