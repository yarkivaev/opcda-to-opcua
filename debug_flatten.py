# -*- coding: utf-8 -*-
from __future__ import print_function
import OpenOPC

opc = OpenOPC.client()
opc.connect('OPCDataStore.TOPCElemerServer.2')

def flatten(client, prefix, depth=0):
    result = []
    indent = "  " * depth
    if prefix:
        children = client.list(prefix)
    else:
        children = client.list()
    f.write("%slist(%r) -> %r\n" % (indent, prefix, children[:5]))
    for child in children[:3]:
        if prefix and child.startswith(prefix + "."):
            full = child
        elif prefix:
            full = "%s.%s" % (prefix, child)
        else:
            full = child
        f.write("%s  child=%r, full=%r\n" % (indent, child, full))
        subchildren = client.list(full)
        f.write("%s  subchildren=%r\n" % (indent, subchildren[:5]))
        if subchildren and subchildren != [full]:
            result.extend(flatten(client, full, depth + 1))
        else:
            f.write("%s  -> LEAF: %r\n" % (indent, full))
            result.append(full)
    return result

f = open('debug_output.txt', 'wb')
f.write("=== Debug flatten ===\n")
tags = flatten(opc, "COM1")
f.write("\n=== Result (first 10) ===\n")
for t in tags[:10]:
    f.write("%r\n" % t)
f.close()

opc.close()
print("Output saved to debug_output.txt")
