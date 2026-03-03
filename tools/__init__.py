"""
Coursework Research Agent — Tools Package

Available tools:
- web_search:     Search Semantic Scholar, arXiv, and OpenLibrary
- wolfram_query:  Wolfram Alpha symbolic math solving
- book_finder:    Find textbooks by topic (OpenLibrary + Google Books)
- latex_renderer: Format and render LaTeX output
"""

from tools.web_search import search_all, search_semantic_scholar, search_arxiv, search_openlibrary, format_results
from tools.wolfram_query import query_wolfram_full, query_wolfram_short, solve_equation, compute_integral, compute_derivative, compute_eigenvalues, solve_ode, format_wolfram_result
from tools.book_finder import find_books, match_known_textbooks, search_openlibrary_books, search_google_books, format_book_results
from tools.latex_renderer import build_solution, build_document, wrap_inline_math, wrap_display_math, wrap_aligned, wrap_cases, format_matrix, format_vector, latex_to_readable

__all__ = [
    # web_search
    "search_all", "search_semantic_scholar", "search_arxiv", "search_openlibrary", "format_results",
    # wolfram_query
    "query_wolfram_full", "query_wolfram_short", "solve_equation", "compute_integral",
    "compute_derivative", "compute_eigenvalues", "solve_ode", "format_wolfram_result",
    # book_finder
    "find_books", "match_known_textbooks", "search_openlibrary_books", "search_google_books", "format_book_results",
    # latex_renderer
    "build_solution", "build_document", "wrap_inline_math", "wrap_display_math",
    "wrap_aligned", "wrap_cases", "format_matrix", "format_vector", "latex_to_readable",
]
