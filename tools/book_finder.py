"""
Book Finder Tool — OpenLibrary & Google Books Lookup
Finds textbooks by topic with edition details, availability, and
chapter-level information when possible.
"""

import json
import urllib.parse
from dataclasses import dataclass
from typing import Optional

import requests

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class BookResult:
    """A single textbook search result."""
    title: str
    authors: str
    year: Optional[int]
    publisher: Optional[str]
    isbn: Optional[str]
    editions: int
    url: str
    source: str               # "OpenLibrary" | "Google Books"
    subjects: list[str]
    preview_available: bool
    description: str


# ---------------------------------------------------------------------------
# Known textbook database (for fast matching)
# ---------------------------------------------------------------------------

KNOWN_TEXTBOOKS: dict[str, dict] = {
    # Mechanics
    "hibbeler statics": {
        "title": "Engineering Mechanics: Statics",
        "authors": "R.C. Hibbeler",
        "topics": ["statics", "equilibrium", "free body diagram", "moment", "truss", "friction"],
    },
    "hibbeler dynamics": {
        "title": "Engineering Mechanics: Dynamics",
        "authors": "R.C. Hibbeler",
        "topics": ["dynamics", "kinematics", "kinetics", "work energy", "impulse momentum"],
    },
    "meriam kraige": {
        "title": "Engineering Mechanics: Statics and Dynamics",
        "authors": "J.L. Meriam, L.G. Kraige",
        "topics": ["statics", "dynamics", "equilibrium", "kinematics", "kinetics"],
    },
    "beer johnston": {
        "title": "Vector Mechanics for Engineers",
        "authors": "F.P. Beer, E.R. Johnston",
        "topics": ["statics", "dynamics", "vectors", "force systems", "rigid body"],
    },
    "taylor classical mechanics": {
        "title": "Classical Mechanics",
        "authors": "John R. Taylor",
        "topics": ["lagrangian", "hamiltonian", "oscillations", "central force", "rigid body rotation"],
    },
    "hibbeler materials": {
        "title": "Mechanics of Materials",
        "authors": "R.C. Hibbeler",
        "topics": ["stress", "strain", "bending", "torsion", "beams", "columns"],
    },
    # Physics
    "serway": {
        "title": "Physics for Scientists and Engineers",
        "authors": "R.A. Serway, J.W. Jewett",
        "topics": ["mechanics", "thermodynamics", "electromagnetism", "optics", "modern physics"],
    },
    "halliday resnick": {
        "title": "Fundamentals of Physics",
        "authors": "D. Halliday, R. Resnick, J. Walker",
        "topics": ["mechanics", "thermodynamics", "electromagnetism", "waves", "quantum"],
    },
    "griffiths electrodynamics": {
        "title": "Introduction to Electrodynamics",
        "authors": "D.J. Griffiths",
        "topics": ["electrostatics", "magnetostatics", "maxwell equations", "electromagnetic waves"],
    },
    "kleppner kolenkow": {
        "title": "An Introduction to Mechanics",
        "authors": "D. Kleppner, R.J. Kolenkow",
        "topics": ["newton laws", "energy", "momentum", "angular momentum", "rigid body", "relativity"],
    },
    "cengel thermodynamics": {
        "title": "Thermodynamics: An Engineering Approach",
        "authors": "Y.A. Çengel, M.A. Boles",
        "topics": ["thermodynamics", "energy", "entropy", "cycles", "heat transfer"],
    },
    # Mathematics
    "kreyszig": {
        "title": "Advanced Engineering Mathematics",
        "authors": "Erwin Kreyszig",
        "topics": ["ode", "pde", "linear algebra", "fourier", "complex analysis", "numerical methods"],
    },
    "stroud": {
        "title": "Engineering Mathematics",
        "authors": "K.A. Stroud",
        "topics": ["calculus", "algebra", "ode", "laplace", "fourier", "statistics"],
    },
    "stewart calculus": {
        "title": "Calculus: Early Transcendentals",
        "authors": "James Stewart",
        "topics": ["limits", "derivatives", "integrals", "series", "multivariable calculus"],
    },
    "strang linear algebra": {
        "title": "Linear Algebra and Its Applications",
        "authors": "Gilbert Strang",
        "topics": ["matrices", "eigenvalues", "vector spaces", "orthogonality", "svd"],
    },
    "boyce diprima": {
        "title": "Elementary Differential Equations and Boundary Value Problems",
        "authors": "W.E. Boyce, R.C. DiPrima",
        "topics": ["first order ode", "second order ode", "laplace transform", "series solutions", "boundary value"],
    },
}


def match_known_textbooks(query: str) -> list[dict]:
    """
    Match a query against the known textbook database.
    Returns textbooks whose topics overlap with the query terms.
    """
    query_lower = query.lower()
    query_terms = set(query_lower.split())
    matches = []

    for key, book in KNOWN_TEXTBOOKS.items():
        # Check if query terms overlap with book topics or key
        topic_set = set(" ".join(book["topics"]).split())
        overlap = query_terms & (topic_set | set(key.split()))
        if overlap:
            score = len(overlap) / max(len(query_terms), 1)
            matches.append({**book, "relevance_score": score, "matched_topics": list(overlap)})

    matches.sort(key=lambda x: x["relevance_score"], reverse=True)
    return matches[:5]


# ---------------------------------------------------------------------------
# 1. OpenLibrary Search
# ---------------------------------------------------------------------------

OPENLIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
OPENLIBRARY_BOOK_URL = "https://openlibrary.org"

def search_openlibrary_books(
    query: str,
    limit: int = 5,
) -> list[BookResult]:
    """
    Search OpenLibrary for textbooks.

    Args:
        query: Topic-based query, e.g. "engineering mechanics statics"
        limit: Max results.
    """
    params = {
        "q": query,
        "limit": limit,
        "fields": "title,author_name,first_publish_year,key,subject,publisher,isbn,edition_count",
    }

    try:
        resp = requests.get(OPENLIBRARY_SEARCH_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, json.JSONDecodeError) as exc:
        print(f"[OpenLibrary] Request failed: {exc}")
        return []

    results: list[BookResult] = []
    for doc in data.get("docs", [])[:limit]:
        isbns = doc.get("isbn") or []
        publishers = doc.get("publisher") or []
        subjects = doc.get("subject") or []

        results.append(BookResult(
            title=doc.get("title", "Untitled"),
            authors=", ".join((doc.get("author_name") or [])[:4]),
            year=doc.get("first_publish_year"),
            publisher=publishers[0] if publishers else None,
            isbn=isbns[0] if isbns else None,
            editions=doc.get("edition_count", 0),
            url=f"{OPENLIBRARY_BOOK_URL}{doc.get('key', '')}",
            source="OpenLibrary",
            subjects=subjects[:10],
            preview_available=False,
            description=f"Subjects: {', '.join(subjects[:6])}" if subjects else "No subjects listed.",
        ))
    return results


# ---------------------------------------------------------------------------
# 2. Google Books Search (no API key required for basic search)
# ---------------------------------------------------------------------------

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"

def search_google_books(
    query: str,
    limit: int = 5,
) -> list[BookResult]:
    """
    Search Google Books for textbooks.

    Args:
        query: Topic-based query.
        limit: Max results.
    """
    params = {
        "q": query,
        "maxResults": limit,
        "printType": "books",
        "orderBy": "relevance",
    }

    try:
        resp = requests.get(GOOGLE_BOOKS_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, json.JSONDecodeError) as exc:
        print(f"[Google Books] Request failed: {exc}")
        return []

    results: list[BookResult] = []
    for item in data.get("items", [])[:limit]:
        info = item.get("volumeInfo", {})
        access = item.get("accessInfo", {})
        isbns = info.get("industryIdentifiers") or []
        isbn = None
        for ident in isbns:
            if ident.get("type") == "ISBN_13":
                isbn = ident.get("identifier")
                break
        if not isbn and isbns:
            isbn = isbns[0].get("identifier")

        results.append(BookResult(
            title=info.get("title", "Untitled"),
            authors=", ".join(info.get("authors") or ["Unknown"]),
            year=int(info.get("publishedDate", "0")[:4]) if info.get("publishedDate") else None,
            publisher=info.get("publisher"),
            isbn=isbn,
            editions=0,
            url=info.get("infoLink", ""),
            source="Google Books",
            subjects=info.get("categories") or [],
            preview_available=access.get("viewability", "") in ("PARTIAL", "ALL_PAGES"),
            description=info.get("description", "No description.")[:400],
        ))
    return results


# ---------------------------------------------------------------------------
# Unified book search
# ---------------------------------------------------------------------------

def find_books(
    query: str,
    limit_per_source: int = 5,
    include_known: bool = True,
) -> dict:
    """
    Comprehensive book search: known textbooks + OpenLibrary + Google Books.

    Args:
        query:            Topic query, e.g. "moment of inertia statics"
        limit_per_source: Max results per API source.
        include_known:    Also match against the built-in known textbook DB.

    Returns:
        Dict with keys: known_matches, openlibrary, google_books
    """
    result = {}

    if include_known:
        result["known_matches"] = match_known_textbooks(query)

    result["openlibrary"] = search_openlibrary_books(query, limit=limit_per_source)
    result["google_books"] = search_google_books(query, limit=limit_per_source)

    return result


def format_book_results(results: dict) -> str:
    """Pretty-print combined book search results."""
    lines: list[str] = []

    # Known textbook matches
    known = results.get("known_matches", [])
    if known:
        lines.append("## 📖 Known Textbook Matches\n")
        for i, book in enumerate(known, 1):
            topics = ", ".join(book.get("matched_topics", []))
            score = book.get("relevance_score", 0)
            lines.append(
                f"**{i}. {book['title']}** by {book['authors']}\n"
                f"   Matched topics: {topics} (score: {score:.2f})\n"
            )

    # OpenLibrary
    ol_books = results.get("openlibrary", [])
    if ol_books:
        lines.append("\n## 🌐 OpenLibrary Results\n")
        for i, b in enumerate(ol_books, 1):
            lines.append(
                f"**{i}. {b.title}** by {b.authors} ({b.year or 'N/A'})\n"
                f"   Publisher: {b.publisher or 'N/A'} | ISBN: {b.isbn or 'N/A'}\n"
                f"   {b.description}\n"
                f"   URL: {b.url}\n"
            )

    # Google Books
    gb_books = results.get("google_books", [])
    if gb_books:
        lines.append("\n## 📚 Google Books Results\n")
        for i, b in enumerate(gb_books, 1):
            preview = "✅ Preview" if b.preview_available else "❌ No preview"
            lines.append(
                f"**{i}. {b.title}** by {b.authors} ({b.year or 'N/A'})\n"
                f"   Publisher: {b.publisher or 'N/A'} | ISBN: {b.isbn or 'N/A'} | {preview}\n"
                f"   {b.description[:200]}\n"
                f"   URL: {b.url}\n"
            )

    return "\n".join(lines) if lines else "No books found."


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "engineering mechanics statics moment"
    print(f"📚 Searching books for: {query}\n")

    results = find_books(query, limit_per_source=3)
    print(format_book_results(results))
