#!/usr/bin/env python3
"""
Scripture AI Bible Database Seeding Script

Run this ONCE to load all Bible verses and Strong's numbers:
    $ python seed_bible.py

This will:
1. Create all database tables
2. Load 31,102 KJV verses
3. Extract ~8,000 Hebrew words with Strong's numbers
4. Create ~780,000 word-to-verse links

Takes 1-2 minutes. Only run once.
"""

from app.seed import seed_database

if __name__ == "__main__":
    print("\n" + "="*60)
    print("SCRIPTURE AI - BIBLE DATABASE SEEDING")
    print("="*60 + "\n")
    
    print("Make sure you have kjv_with_strongs.json in this directory!")
    print("Download from: https://github.com/openbibleinfo/Bible-datasets\n")
    
    try:
        seed_database()
        print("\n" + "="*60)
        print("✓ SUCCESS! Your Bible database is ready!")
        print("="*60)
        print("\nYou can now:")
        print("  1. Run: python main.py")
        print("  2. Visit: http://localhost:8000/docs")
        print("  3. Build your API endpoints!\n")
    except FileNotFoundError:
        print("\n❌ ERROR: kjv_with_strongs.json not found!")
        print("Download it and place in project root.\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
