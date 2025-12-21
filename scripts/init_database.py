#!/usr/bin/env python3
"""
Initialize the DeadStream database.

Creates the shows.db file with proper schema.
Safe to run multiple times.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import init_database, verify_database

if __name__ == "__main__":
    print("Initializing DeadStream database...\n")
    
    success = init_database()
    
    if success:
        print("\nVerifying database...\n")
        verify_database()
    else:
        print("\nDatabase initialization failed!")
        sys.exit(1)
