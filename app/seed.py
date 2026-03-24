"""
Bible database seeding script
Load KJV+ with Strong's numbers into PostgreSQL
"""

import json
import re
import sys
from sqlmodel import Session, create_engine
from app.models import Verse, Lexicon, VerseWordLink, SQLModel
from app.config import settings

# Create engine
engine = create_engine(settings.DATABASE_URL, echo=False)

def parse_kjv_plus_text(text_with_strongs: str) -> list:
    """
    Parse KJV+ format: 'In[H853] the[H853] beginning[H7225]'
    
    Returns list of tuples: [(word_text, strongs_id), ...]
    
    Args:
        text_with_strongs: Text with Strong's numbers embedded
        
    Returns:
        List of (word, strongs_id) tuples
    """
    pattern = r'([^\[]+)\[(H\d+)\]'
    matches = re.findall(pattern, text_with_strongs)
    return [(word.strip(), strongs_id) for word, strongs_id in matches]

def get_clean_verse_text(text_with_strongs: str) -> str:
    """
    Remove Strong's codes to get clean verse text
    
    Args:
        text_with_strongs: Text with [Hxxxx] codes
        
    Returns:
        Clean text without codes
    """
    clean = re.sub(r'\[H\d+\]', '', text_with_strongs)
    return re.sub(r'\s+', ' ', clean).strip()

def seed_database(kjv_file: str = None):
    """
    Load Bible data from KJV+ JSON file into database
    
    Args:
        kjv_file: Path to KJV+ JSON file
    """
    if kjv_file is None:
        kjv_file = settings.KJV_PLUS_FILE
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    print("✓ Database tables created\n")
    
    # Load JSON
    print(f"Loading {kjv_file}...")
    try:
        with open(kjv_file, "r", encoding="utf-8") as f:
            bible_data = json.load(f)
        print("✓ Loaded JSON\n")
    except FileNotFoundError:
        print(f"ERROR: {kjv_file} not found!")
        print("Download from: https://github.com/openbibleinfo/Bible-datasets")
        sys.exit(1)
    
    # Parse data
    print("Parsing verses and extracting Strong's numbers...\n")
    
    verses_to_add = []
    lexicon_entries = {}
    word_links = []
    
    verse_counter = 0
    total_word_links = 0
    
    # Iterate through Bible structure
    for book_name, chapters in bible_data.items():
        for chapter_num, verses_dict in chapters.items():
            for verse_num, verse_text_with_strongs in verses_dict.items():
                verse_counter += 1
                
                # Build reference
                reference = f"{book_name} {chapter_num}:{verse_num}"
                clean_text = get_clean_verse_text(verse_text_with_strongs)
                
                # Create Verse
                verse = Verse(
                    id=verse_counter,
                    reference=reference,
                    text_content=clean_text
                )
                verses_to_add.append(verse)
                
                # Parse words and Strong's
                words_with_strongs = parse_kjv_plus_text(verse_text_with_strongs)
                
                # Create VerseWordLink entries
                # word_index is CRITICAL - it's the position in the verse
                for word_index, (word_text, strongs_id) in enumerate(words_with_strongs):
                    link = VerseWordLink(
                        verse_id=verse_counter,
                        strongs_id=strongs_id,
                        word_index=word_index,  # 0, 1, 2, 3, ... (position)
                        word_text=word_text
                    )
                    word_links.append(link)
                    total_word_links += 1
                    
                    # Track unique Strong's IDs
                    if strongs_id not in lexicon_entries:
                        lexicon_entries[strongs_id] = {
                            'strongs_id': strongs_id,
                            'hebrew_word': '',
                            'transliteration': '',
                            'definition': f"Strong's {strongs_id}"
                        }
    
    print(f"✓ Parsed {verse_counter} verses")
    print(f"✓ Extracted {len(lexicon_entries)} unique Strong's IDs")
    print(f"✓ Created {total_word_links} word links\n")
    
    # Insert into database
    print("Inserting data into database...\n")
    
    # Step 1: Verses
    print("  [1/3] Inserting verses...")
    with Session(engine) as session:
        session.add_all(verses_to_add)
        session.commit()
    print(f"  ✓ {len(verses_to_add)} verses\n")
    
    # Step 2: Lexicon
    print("  [2/3] Creating lexicon entries...")
    lexicon_list = [Lexicon(**entry) for entry in lexicon_entries.values()]
    with Session(engine) as session:
        session.add_all(lexicon_list)
        session.commit()
    print(f"  ✓ {len(lexicon_list)} entries\n")
    
    # Step 3: Word Links (JUNCTION TABLE)
    print("  [3/3] Inserting word links (junction table)...")
    with Session(engine) as session:
        session.add_all(word_links)
        session.commit()
    print(f"  ✓ {len(word_links)} links\n")
    
    print("="*60)
    print("✓ DATABASE SEEDING COMPLETE!")
    print("="*60)
    print(f"\nStats:")
    print(f"  Verses: {len(verses_to_add)}")
    print(f"  Lexicon entries: {len(lexicon_list)}")
    print(f"  Word links: {len(word_links)}")
    print(f"\nYour Scripture AI database is ready!\\n")

if __name__ == "__main__":
    seed_database()
