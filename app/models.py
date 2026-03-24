"""
SQLModel definitions for Scripture AI
All database models with relationships
"""

from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

# ============= SCRIPTURE MODELS =============

class Verse(SQLModel, table=True):
    \"\"\"
    Bible verse table
    Stores the actual scripture text with reference
    \"\"\"
    id: Optional[int] = Field(default=None, primary_key=True)
    reference: str = Field(index=True)  # e.g., "Genesis 1:1"
    text_content: str  # The actual verse text

    # Relationships
    word_links: List["VerseWordLink"] = Relationship(back_populates="verse")
    notes: List["Note"] = Relationship(back_populates="verse")
    study_sessions: List["StudySession"] = Relationship(back_populates="verse")

    def __repr__(self) -> str:
        return f"<Verse {self.reference}>"


class Lexicon(SQLModel, table=True):
    \"\"\"
    Hebrew/Greek word dictionary
    Stores Strong's numbers and definitions
    \"\"\"
    strongs_id: str = Field(primary_key=True)  # e.g., "H430"
    hebrew_word: str  # e.g., "אלהים"
    transliteration: str  # e.g., "elohim"
    definition: str  # Full definition

    # Relationships
    links: List["VerseWordLink"] = Relationship(back_populates="lexicon")

    def __repr__(self) -> str:
        return f"<Lexicon {self.strongs_id} ({self.transliteration})>"


class VerseWordLink(SQLModel, table=True):
    \"\"\"
    Junction table linking verses to words
    Many-to-Many relationship with word index
    
    Composite Primary Key: (verse_id, strongs_id, word_index)
    This means:
    - Same verse can have same word at different positions
    - Example: "God God" → two rows with different word_index
    \"\"\"
    verse_id: int = Field(foreign_key="verse.id", primary_key=True)
    strongs_id: str = Field(foreign_key="lexicon.strongs_id", primary_key=True)
    word_index: int = Field(primary_key=True)  # Position in verse (0, 1, 2, ...)
    word_text: str  # The actual word as it appears in verse

    # Relationships
    verse: Verse = Relationship(back_populates="word_links")
    lexicon: Lexicon = Relationship(back_populates="links")

    def __repr__(self) -> str:
        return f"<VerseWordLink {self.strongs_id} at index {self.word_index}>"


# ============= USER & STUDY MODELS =============

class User(SQLModel, table=True):
    \"\"\"
    User account for Scripture AI
    Stores authentication information
    \"\"\"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    notes: List["Note"] = Relationship(back_populates="user")
    study_sessions: List["StudySession"] = Relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class Note(SQLModel, table=True):
    \"\"\"
    User's personal notes on a verse
    One-to-Many: User has many notes
    One-to-Many: Verse has many notes
    \"\"\"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    verse_id: int = Field(foreign_key="verse.id")
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="notes")
    verse: Verse = Relationship(back_populates="notes")

    def __repr__(self) -> str:
        return f"<Note user={self.user_id} verse={self.verse_id}>"


class StudySession(SQLModel, table=True):
    \"\"\"
    Track when a user studies a verse
    Many-to-Many: Users study many verses, verses studied by many users
    \"\"\"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    verse_id: int = Field(foreign_key="verse.id")
    studied_at: datetime = Field(default_factory=datetime.utcnow)
    duration_seconds: int = 0  # How long they studied

    # Relationships
    user: User = Relationship(back_populates="study_sessions")
    verse: Verse = Relationship(back_populates="study_sessions")

    def __repr__(self) -> str:
        return f"<StudySession user={self.user_id} verse={self.verse_id}>"


# ============= SCHEMA SUMMARY =============
\"\"\"
Schema Overview:

VERSE (Scripture Data)
  ├── id (PK)
  ├── reference (indexed)
  └── text_content

LEXICON (Word Dictionary)
  ├── strongs_id (PK)
  ├── hebrew_word
  ├── transliteration
  └── definition

VERSEWORDLINK (Junction Table - Many-to-Many)
  ├── verse_id (FK, PK)
  ├── strongs_id (FK, PK)
  ├── word_index (PK) - Position in verse
  └── word_text

USER (Authentication)
  ├── id (PK)
  ├── email (unique, indexed)
  ├── hashed_password
  └── created_at

NOTE (Personal Study)
  ├── id (PK)
  ├── user_id (FK)
  ├── verse_id (FK)
  ├── content
  ├── created_at
  └── updated_at

STUDYSESSION (Study Tracking)
  ├── id (PK)
  ├── user_id (FK)
  ├── verse_id (FK)
  ├── studied_at
  └── duration_seconds

Relationships:
- Verse ↔ VerseWordLink (1:M)
- Lexicon ↔ VerseWordLink (1:M)
- Verse ↔ Lexicon (M:M through VerseWordLink)
- User ↔ Note (1:M)
- Verse ↔ Note (1:M)
- User ↔ StudySession (1:M)
- Verse ↔ StudySession (1:M)
\"\"\"
