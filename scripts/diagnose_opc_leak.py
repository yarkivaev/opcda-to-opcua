# -*- coding: utf-8 -*-
"""
OpenOPC memory leak diagnostic.

Measures actual process memory during OPC reads to identify COM leaks.
Run on Windows with OpenOPC installed.

Usage: python scripts/diagnose_opc_leak.py <progid> <host> <tag>
Example: python scripts/diagnose_opc_leak.py "Matrikon.OPC.Simulation" "localhost" "Random.Int1"
"""
from __future__ import print_function

import gc
import sys
import time

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    import win32api
    import win32process
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False


def get_memory_mb():
    """Get current process memory in MB."""
    if HAS_PSUTIL:
        import os
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)
    elif HAS_WIN32:
        import win32process
        handle = win32api.GetCurrentProcess()
        info = win32process.GetProcessMemoryInfo(handle)
        return info["WorkingSetSize"] / (1024 * 1024)
    else:
        return 0


def test_reads_without_cleanup(client, tag, count):
    """Perform reads without recreating client."""
    for _ in range(count):
        client.read(tag, sync=True)


def test_reads_with_gc(client, tag, count, gc_every):
    """Perform reads with periodic gc.collect()."""
    for i in range(count):
        client.read(tag, sync=True)
        if (i + 1) % gc_every == 0:
            gc.collect()


def main():
    if len(sys.argv) < 4:
        print("Usage: python diagnose_opc_leak.py <progid> <host> <tag>")
        print("Example: python diagnose_opc_leak.py Matrikon.OPC.Simulation localhost Random.Int1")
        sys.exit(1)
    progid = sys.argv[1]
    host = sys.argv[2]
    tag = sys.argv[3]
    if not HAS_PSUTIL and not HAS_WIN32:
        print("WARNING: Cannot measure memory - install psutil or pywin32")
        print("")
    print("OpenOPC Memory Leak Diagnostic")
    print("=" * 60)
    print("Server: %s @ %s" % (progid, host))
    print("Tag: %s" % tag)
    print("=" * 60)
    print("")
    import pythoncom
    import OpenOPC
    pythoncom.CoInitialize()
    print("TEST 1: 1000 reads without cleanup")
    print("-" * 60)
    client = OpenOPC.client()
    client.connect(progid, host)
    gc.collect()
    mem_before = get_memory_mb()
    print("Memory before: %.2f MB" % mem_before)
    test_reads_without_cleanup(client, tag, 1000)
    gc.collect()
    mem_after = get_memory_mb()
    print("Memory after:  %.2f MB" % mem_after)
    print("Growth:        %.2f MB" % (mem_after - mem_before))
    client.close()
    print("")
    print("TEST 2: 1000 reads with gc.collect() every 100")
    print("-" * 60)
    client = OpenOPC.client()
    client.connect(progid, host)
    gc.collect()
    mem_before = get_memory_mb()
    print("Memory before: %.2f MB" % mem_before)
    test_reads_with_gc(client, tag, 1000, 100)
    gc.collect()
    mem_after = get_memory_mb()
    print("Memory after:  %.2f MB" % mem_after)
    print("Growth:        %.2f MB" % (mem_after - mem_before))
    client.close()
    print("")
    print("TEST 3: 1000 reads with client recreation every 100")
    print("-" * 60)
    client = OpenOPC.client()
    client.connect(progid, host)
    gc.collect()
    mem_before = get_memory_mb()
    print("Memory before: %.2f MB" % mem_before)
    for i in range(1000):
        client.read(tag, sync=True)
        if (i + 1) % 100 == 0:
            client.close()
            gc.collect()
            client = OpenOPC.client()
            client.connect(progid, host)
    gc.collect()
    mem_after = get_memory_mb()
    print("Memory after:  %.2f MB" % mem_after)
    print("Growth:        %.2f MB" % (mem_after - mem_before))
    client.close()
    print("")
    print("TEST 4: 5000 reads without cleanup (stress test)")
    print("-" * 60)
    client = OpenOPC.client()
    client.connect(progid, host)
    gc.collect()
    mem_before = get_memory_mb()
    print("Memory before: %.2f MB" % mem_before)
    for i in range(5000):
        client.read(tag, sync=True)
        if (i + 1) % 1000 == 0:
            gc.collect()
            mem_now = get_memory_mb()
            print("After %d reads: %.2f MB (+%.2f)" % (i + 1, mem_now, mem_now - mem_before))
    client.close()
    print("")
    print("=" * 60)
    print("CONCLUSION:")
    print("If TEST 3 shows less growth than TEST 1/2, client recreation helps.")
    print("If TEST 4 shows linear growth, OpenOPC is leaking COM objects.")
    print("=" * 60)
    pythoncom.CoUninitialize()


if __name__ == "__main__":
    main()
