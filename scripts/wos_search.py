"""Query Web of Science Starter without printing or storing an API key."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path


API_BASE = "https://api.clarivate.com/apis/wos-starter/v2/documents"


def parse_key_text(content: str) -> str | None:
    for line in content.splitlines():
        match = re.match(r"^\s*(?:WOS_STARTER_API_KEY\s*=|APIkey\s*:)\s*(.*?)\s*$", line, re.I)
        if match:
            value = match.group(1).strip().strip('"\'')
            if value and not re.search(r"\s", value):
                return value
    return None


def load_key(profile: dict, environ: dict | None = None) -> str | None:
    config = (profile.get("sources") or {}).get("wos") or {}
    variables = os.environ if environ is None else environ
    env_name = config.get("api_key_env") or "WOS_STARTER_API_KEY"
    if variables.get(env_name):
        return variables[env_name].strip()
    key_file = config.get("api_key_file")
    if key_file:
        path = Path(key_file).expanduser()
        if path.is_file():
            return parse_key_text(path.read_text(encoding="utf-8-sig"))
    return None


def query_wos(profile: dict, query: str, start: str, end: str, limit: int = 20) -> dict:
    first = date.fromisoformat(start)
    last = date.fromisoformat(end)
    if first > last or not 1 <= limit <= 50 or not query.strip():
        raise ValueError("Invalid query, date range, or limit")
    key = load_key(profile)
    base = {"source": "Web of Science Starter API", "query": query, "start": start, "end": end}
    if not key:
        return {**base, "status": "not_configured", "total": None, "hits": []}
    params = {"db": "WOS", "q": query, "limit": limit, "publishTimeSpan": f"{start} {end}"}
    url = API_BASE + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"X-ApiKey": key, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        return {**base, "status": "http_error", "http_status": exc.code, "total": None, "hits": []}
    except (urllib.error.URLError, OSError):
        return {**base, "status": "network_error", "total": None, "hits": []}
    hits = []
    for item in payload.get("hits") or []:
        source = item.get("source") or {}
        hits.append({
            "uid": item.get("uid"),
            "title": item.get("title"),
            "doi": (item.get("identifiers") or {}).get("doi"),
            "journal": source.get("sourceTitle"),
            "year": source.get("publishYear"),
            "month": source.get("publishMonth"),
            "record_url": (item.get("links") or {}).get("record"),
        })
    return {**base, "status": "ok", "total": (payload.get("metadata") or {}).get("total"), "hits": hits}


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the Web of Science Starter API using a private profile")
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--query", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    profile = json.loads(args.profile.expanduser().read_text(encoding="utf-8-sig"))
    result = query_wos(profile, args.query, args.start, args.end, args.limit)
    content = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
        print(json.dumps({"status": result["status"]}))
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(content, end="")
    return 0 if result["status"] in {"ok", "not_configured"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
