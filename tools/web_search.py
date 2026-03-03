"""
Web Search Tool — Semantic Scholar, arXiv, and OpenLibrary
Searches for academic papers, preprints, and textbooks related to
mechanics, physics, and mathematics coursework problems.
"""

import json
import re
import urllib.parse
from dataclasses import dataclass, asdict
from typing import Optional

import requests

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class SearchResult:
    """A single search result from any backend."""
    title: str
    authors: str
    year: Optional[int]
    url: str
    source: str          # "Semantic Scholar" | "arXiv" | "OpenLibrary"
    snippet: str         # relevance snippet / abstract excerpt
    has_examples: bool   # heuristic: likely contains worked examples


def _looks_like_examples(text: str) -> bool:
    """Heuristic: does the text suggest worked examples are present?"""
    markers = [
        "worked example", "solved problem", "example ",
        "step-by-step", "solution", "exercise", "illustration",
        "sample problem", "tutorial", "practice problem",
    ]
    lower = text.lower()
    return any(m in lower for m in markers)


# ---------------------------------------------------------------------------
# 1. Semantic Scholar API (free, no key)
# ---------------------------------------------------------------------------

SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def search_semantic_scholar(
    query: str,
    limit: int = 5,
    year_range: Optional[str] = None,
) -> list[SearchResult]:
    """
    Search Semantic Scholar for academic papers.

    Args:
        query:      Natural-language query, e.g.
                    "worked example moment of inertia composite body"
        limit:      Max results to return.
        year_range: Optional year filter, e.g. "2000-2024".
    """
    params: dict = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,url,abstract,externalIds",
    }
    if year_range:
        params["year"] = year_range

    try:
        resp = requests.get(SEMANTIC_SCHOLAR_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, json.JSONDecodeError) as exc:
        print(f"[Semantic Scholar] Request failed: {exc}")
        return []

    results: list[SearchResult] = []
    for paper in data.get("data", []):
        abstract = paper.get("abstract") or ""
        snippet = abstract[:300] + ("…" if len(abstract) > 300 else "")
        authors_list = paper.get("authors") or []
        authors_str = ", ".join(a.get("name", "") for a in authors_list[:4])
        if len(authors_list) > 4:
            authors_str += " et al."

        paper_url = paper.get("url") or ""
        # Try to get a DOI link if available
        ext_ids = paper.get("externalIds") or {}
        if ext_ids.get("DOI"):
            paper_url = f"https://doi.org/{ext_ids['DOI']}"

        results.append(SearchResult(
            title=paper.get("title", "Untitled"),
            authors=authors_str,
            year=paper.get("year"),
            url=paper_url,
            source="Semantic Scholar",
            snippet=snippet,
            has_examples=_looks_like_examples(abstract),
        ))
    return results


# ---------------------------------------------------------------------------
# 2. arXiv API (free)
# ---------------------------------------------------------------------------

ARXIV_API_URL = "http://export.arxiv.org/api/query"

def search_arxiv(
    query: str,
    limit: int = 5,
    categories: Optional[list[str]] = None,
) -> list[SearchResult]:
    """
    Search arXiv for physics / math preprints.

    Args:
        query:      Natural-language search query.
        limit:      Max results.
        categories: Optional arXiv category filters,
                    e.g. ["physics.class-ph", "math.NA"].
    """
    search_query = f"all:{query}"
    if categories:
        cat_filter = " OR ".join(f"cat:{c}" for c in categories)
        search_query = f"({search_query}) AND ({cat_filter})"

    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": limit,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }

    try:
        resp = requests.get(ARXIV_API_URL, params=params, timeout=15)
        resp.raise_for_status()
        body = resp.text
    except requests.RequestException as exc:
        print(f"[arXiv] Request failed: {exc}")
        return []

    results: list[SearchResult] = []

    # Lightweight XML parsing (avoid lxml dependency)
    entries = re.findall(r"<entry>(.*?)</entry>", body, re.DOTALL)
    for entry in entries:
        title_m = re.search(r"<title>(.*?)</title>", entry, re.DOTALL)
        summary_m = re.search(r"<summary>(.*?)</summary>", entry, re.DOTALL)
        link_m = re.search(r'<id>(.*?)</id>', entry)
        published_m = re.search(r"<published>(\d{4})", entry)

        author_names = re.findall(r"<name>(.*?)</name>", entry)

        title = title_m.group(1).strip().replace("\n", " ") if title_m else "Untitled"
        summary = summary_m.group(1).strip().replace("\n", " ") if summary_m else ""
        snippet = summary[:300] + ("…" if len(summary) > 300 else "")
        url = link_m.group(1).strip() if link_m else ""
        year = int(published_m.group(1)) if published_m else None
        authors_str = ", ".join(author_names[:4])
        if len(author_names) > 4:
            authors_str += " et al."

        results.append(SearchResult(
            title=title,
            authors=authors_str,
            year=year,
            url=url,
            source="arXiv",
            snippet=snippet,
            has_examples=_looks_like_examples(summary),
        ))
    return results


# ---------------------------------------------------------------------------
# 3. OpenLibrary API (free)
# ---------------------------------------------------------------------------

OPENLIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"

def search_openlibrary(
    query: str,
    limit: int = 5,
) -> list[SearchResult]:
    """
    Search OpenLibrary for textbooks matching the query.

    Args:
        query: Topic-based query, e.g. "engineering mechanics statics"
        limit: Max results.
    """
    params = {
        "q": query,
        "limit": limit,
        "fields": "title,author_name,first_publish_year,key,subject,edition_count",
    }

    try:
        resp = requests.get(OPENLIBRARY_SEARCH_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, json.JSONDecodeError) as exc:
        print(f"[OpenLibrary] Request failed: {exc}")
        return []

    results: list[SearchResult] = []
    for doc in data.get("docs", [])[:limit]:
        title = doc.get("title", "Untitled")
        authors_list = doc.get("author_name") or []
        authors_str = ", ".join(authors_list[:4])
        if len(authors_list) > 4:
            authors_str += " et al."
        year = doc.get("first_publish_year")
        key = doc.get("key", "")
        url = f"https://openlibrary.org{key}" if key else ""
        subjects = doc.get("subject") or []
        snippet = f"Subjects: {', '.join(subjects[:8])}" if subjects else "No subjects listed."
        editions = doc.get("edition_count", 0)
        if editions:
            snippet += f" | {editions} edition(s) available."

        results.append(SearchResult(
            title=title,
            authors=authors_str,
            year=year,
            url=url,
            source="OpenLibrary",
            snippet=snippet,
            has_examples=_looks_like_examples(title + " " + " ".join(subjects)),
        ))
    return results


# ---------------------------------------------------------------------------
# Unified search
# ---------------------------------------------------------------------------

def search_all(
    query: str,
    limit_per_source: int = 5,
    examples_only: bool = False,
) -> list[SearchResult]:
    """
    Run a unified search across all three sources.

    Args:
        query:            Natural-language search query.
        limit_per_source: Max results per source.
        examples_only:    If True, only return results likely to have worked examples.

    Returns:
        Combined list of SearchResult sorted by relevance heuristic.
    """
    results: list[SearchResult] = []

    # Augment query for better example-finding
    example_query = f"{query} worked example solved problem"

    # 1. Semantic Scholar (best for papers)
    results.extend(search_semantic_scholar(example_query, limit=limit_per_source))

    # 2. arXiv (best for preprints with derivations)
    results.extend(search_arxiv(query, limit=limit_per_source))

    # 3. OpenLibrary (best for textbooks)
    results.extend(search_openlibrary(query, limit=limit_per_source))

    # Optional filter
    if examples_only:
        results = [r for r in results if r.has_examples]

    # Sort: items with examples first, then by year (newest first)
    results.sort(key=lambda r: (not r.has_examples, -(r.year or 0)))

    return results


def format_results(results: list[SearchResult]) -> str:
    """Pretty-print search results for the agent to consume."""
    if not results:
        return "No results found."

    lines: list[str] = []
    for i, r in enumerate(results, 1):
        example_flag = " ✅ Likely has examples" if r.has_examples else ""
        lines.append(
            f"### [{i}] {r.title}\n"
            f"- **Authors:** {r.authors}\n"
            f"- **Year:** {r.year or 'N/A'}\n"
            f"- **Source:** {r.source}{example_flag}\n"
            f"- **URL:** {r.url}\n"
            f"- **Snippet:** {r.snippet}\n"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point (for manual testing)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "moment of inertia composite body worked example"
    print(f"🔍 Searching for: {query}\n")

    results = search_all(query, limit_per_source=3)
    print(format_results(results))
    print(f"\nTotal results: {len(results)}")
