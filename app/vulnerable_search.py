"""
VULNERABLE SEARCH ENDPOINT - INTENTIONALLY VULNERABLE TO SQL INJECTION

This module contains the deliberately vulnerable search implementation for the CTF challenge.
The vulnerability is isolated to this single route/function.

VULNERABILITY: The search_term is directly concatenated into the SQL query string
without parameterization, allowing UNION-based SQL injection.

MODERATE DIFFICULTY DESIGN:
- The ordinary records query selects 4 columns: id, title, content, category
- The flag is in a SEPARATE table: restricted_records (title, content, classification)
- Participants must: (1) confirm injection, (2) enumerate column count blind (ORDER BY / UNION),
  (3) discover restricted table/column names, (4) construct correct UNION SELECT
- Errors are caught and shown as generic "Invalid search syntax" - no schema leakage
"""

from flask import Blueprint, render_template, request, session, current_app
import sqlite3

bp = Blueprint("vuln_search", __name__, url_prefix="/records")


@bp.route("/search", methods=["GET", "POST"])
def vulnerable_search():
    """
    Intentionally vulnerable search endpoint.
    Constructs query via string concatenation - DO NOT USE THIS PATTERN IN PRODUCTION.
    """
    results = []
    search_term = ""
    error = None

    if request.method == "POST":
        # The whole request path is guarded - query execution AND template
        # rendering. An injected UNION can make the database return a value
        # that the renderer then cannot use, so the failure does not always
        # surface as a sqlite3.Error. Both classes of failure are reported
        # with the identical generic message.
        try:
            search_term = request.form.get("search_term", "").strip()

            if len(search_term) > 200:
                error = "Search term too long"
            else:
                db_path = current_app.config["DATABASE_PATH"]
                conn = None
                try:
                    conn = sqlite3.connect(db_path)
                    conn.row_factory = sqlite3.Row
                    conn.execute("PRAGMA foreign_keys = ON")

                    # VULNERABLE QUERY - String concatenation enables SQL injection
                    # This query selects 4 columns: id, title, content, category
                    query = f"""
                        SELECT id, title, content, category
                        FROM records
                        WHERE title LIKE '%{search_term}%'
                        ORDER BY id
                    """

                    cursor = conn.execute(query)
                    results = cursor.fetchall()

                    if not results:
                        error = "No records found matching your search."
                    elif not all(isinstance(row["id"], int) for row in results):
                        # SQLite does not enforce column types, so a UNION can
                        # hand back a non-numeric value in the id position that
                        # the result renderer cannot use. Such a result set is
                        # unusable rather than something to coerce, so it is
                        # raised and reported through the generic handler below
                        # - identical to a query the database rejected.
                        raise TypeError("result id is not an integer")

                finally:
                    if conn:
                        conn.close()

            return render_template("search.html", results=results, search_term=search_term, error=error)

        except Exception:
            # Generic error message - no schema details leaked, and nothing
            # here distinguishes a rejected query from one the database
            # accepted but whose rows the renderer could not use.
            return render_template("search.html", results=[], search_term=search_term, error="Invalid search syntax.")

    return render_template("search.html", results=results, search_term=search_term, error=error)