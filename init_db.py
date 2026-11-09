#!/usr/bin/env python3
"""
Database initialization script for QueryQuest CTF challenge.
Run this script to initialize or reset the database.
"""
import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.models import init_db, reset_db, get_db_path
from config import Config


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Initialize or reset the QueryQuest database")
    parser.add_argument("--reset", action="store_true", help="Reset database (requires --yes)")
    parser.add_argument("--yes", action="store_true", help="Confirm reset without prompt")
    parser.add_argument("--flag", help="Override flag value (default from env CTF_FLAG or config)")
    args = parser.parse_args()

    db_path = get_db_path()

    if args.reset:
        if not args.yes:
            confirm = input(f"This will DELETE {db_path} and reinitialize. Continue? (y/N): ")
            if confirm.lower() != "y":
                print("Aborted.")
                return 1
        print(f"Resetting database at {db_path}...")
        reset_db(db_path, confirm=True)
        flag = args.flag or Config.FLAG
        init_db(db_path, flag=flag)
        print("Database reset and initialized.")
    else:
        if db_path.exists():
            print(f"Database already exists at {db_path}. Use --reset to reinitialize.")
            return 1
        print(f"Initializing database at {db_path}...")
        flag = args.flag or Config.FLAG
        init_db(db_path, flag=flag)
        print("Database initialized.")

    # Set restrictive permissions on the database file
    try:
        os.chmod(db_path, 0o600)
        print(f"Set database permissions to 600.")
    except Exception as e:
        print(f"Warning: Could not set permissions: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())