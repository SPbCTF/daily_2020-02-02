#!/usr/bin/env python
import base64

data = input()
data_decoded = base64.b64decode(data)

print(data)