"""
boot.py - CircuitPython (Pico / Pico W)
Mounts filesystem as writable so code.py can write log files.
Required — without this, file writes silently fail.
"""
import storage
storage.remount("/", False)
