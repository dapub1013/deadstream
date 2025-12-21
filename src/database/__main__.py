"""
Main entry point for database module.

Allows running: python3 -m src.database
"""

from . import init_database, verify_database

if __name__ == "__main__":
    print("Initializing DeadStream database...\n")
    
    success = init_database()
    
    if success:
        print("\nVerifying database...\n")
        verify_database()
    else:
        print("\nDatabase initialization failed!")
        exit(1)
