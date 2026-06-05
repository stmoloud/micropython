"""boot.py - enable write access to filesystem"""
import storage
storage.remount("/", False)
