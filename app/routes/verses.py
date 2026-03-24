"""
Verse API Endpoints
GET /verses - Search and retrieve verses
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Verse, VerseWordLink, Lexicon

router = APIRouter(
    prefix="/verses",
    tags=["verses"],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
def list_verses(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    """
    Get list of verses with pagination
    
    Query Parameters:
    - skip: Number of verses to skip (default: 0)
    - limit: Number of verses to return (default: 10, max: 100)
    """
    if limit > 100:
        limit = 100
    
    verses = session.exec(
        select(Verse).offset(skip).limit(limit)
    ).all()
    
    return {
        "total": session.exec(select(Verse)).all().__len__(),
        "skip": skip,
        "limit": limit,
        "verses": verses
    }

@router.get("/search")
def search_verses(
    query: str,
    session: Session = Depends(get_session)
):
    """
    Search verses by text content
    
    Example: /verses/search?query=God
    """
    if len(query) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    
    verses = session.exec(
        select(Verse).where(
            Verse.text_content.ilike(f"%{query}%")
        ).limit(20)
    ).all()
    
    return {
        "query": query,
        "count": len(verses),
        "verses": verses
    }

@router.get("/{verse_id}")
def get_verse(
    verse_id: int,
    session: Session = Depends(get_session)
):
    """
    Get a specific verse with all its words and Strong's numbers
    
    Example: /verses/1
    """
    verse = session.get(Verse, verse_id)
    if not verse:
        raise HTTPException(status_code=404, detail="Verse not found")
    
    # Get all words in this verse
    words = session.exec(
        select(VerseWordLink).where(VerseWordLink.verse_id == verse_id)
    ).all()
    
    # Enrich with lexicon data
    enriched_words = []
    for word_link in sorted(words, key=lambda w: w.word_index):
        lexicon = session.get(Lexicon, word_link.strongs_id)
        enriched_words.append({
            "word_index": word_link.word_index,
            "word_text": word_link.word_text,
            "strongs_id": word_link.strongs_id,
            "definition": lexicon.definition if lexicon else "Unknown",
            "hebrew_word": lexicon.hebrew_word if lexicon else "",
            "transliteration": lexicon.transliteration if lexicon else ""
        })
    
    return {
        "id": verse.id,
        "reference": verse.reference,
        "text": verse.text_content,
        "words": enriched_words
    }

@router.get("/reference/{book}/{chapter}/{verse}")
def get_by_reference(
    book: str,
    chapter: int,
    verse: int,
    session: Session = Depends(get_session)
):
    """
    Get verse by book, chapter, verse
    
    Example: /verses/reference/Genesis/1/1
    """
    reference = f"{book} {chapter}:{verse}"
    
    verse_obj = session.exec(
        select(Verse).where(Verse.reference == reference)
    ).first()
    
    if not verse_obj:
        raise HTTPException(status_code=404, detail=f"Verse '{reference}' not found")
    
    return get_verse(verse_obj.id, session)

@router.get("/strongs/{strongs_id}")
def get_by_strongs(
    strongs_id: str,
    session: Session = Depends(get_session)
):
    """
    Find all verses containing a specific Strong's number
    
    Example: /verses/strongs/H430 (all verses with 'God')
    """
    lexicon = session.get(Lexicon, strongs_id)
    if not lexicon:
        raise HTTPException(status_code=404, detail=f"Strong's {strongs_id} not found")
    
    # Get all verses with this word
    word_links = session.exec(
        select(VerseWordLink).where(VerseWordLink.strongs_id == strongs_id)
    ).all()
    
    verses = []
    for link in word_links:
        verse = session.get(Verse, link.verse_id)
        verses.append({
            "verse_id": verse.id,
            "reference": verse.reference,
            "text": verse.text_content,
            "word_position": link.word_index,
            "word_text": link.word_text
        })
    
    return {
        "strongs_id": strongs_id,
        "definition": lexicon.definition,
        "hebrew_word": lexicon.hebrew_word,
        "transliteration": lexicon.transliteration,
        "occurrences": len(verses),
        "verses": verses[:20]  # Limit to 20 for response size
    }
