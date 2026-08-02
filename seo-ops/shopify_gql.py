#!/usr/bin/env python3
"""
The Baking Kaur - shared Admin GraphQL execution for seo-ops scripts.

Two backends, chosen automatically:
  - SHOPIFY_TOKEN set -> direct HTTP POST to the Admin API (the original path every
    seo-ops script used).
  - SHOPIFY_TOKEN unset -> `shopify store execute` via the authenticated Shopify CLI
    session (`shopify store auth --scopes read_products,write_products` once, opens a
    browser). Same Admin GraphQL API, no token typed or stored by this script either way.
    Built when the MCP Shopify connector was down mid-session (Phase 7.6) with no token
    available - proven reusable rather than left as a one-off workaround in a single script.

USAGE
  from shopify_gql import gql
  data = gql("query { shop { name } }")
  data = gql("mutation { ... }", allow_mutations=True)   # only needed for the CLI backend;
                                                          # the HTTP backend has no such flag
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Dict, Optional

import requests

STORE = os.environ.get("SHOPIFY_STORE", "")
TOKEN = os.environ.get("SHOPIFY_TOKEN", "")
API_VERSION = "2025-01"
ENDPOINT = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"

CLI_STORE = os.environ.get("SHOPIFY_STORE_CLI", "ae86ba-2a.myshopify.com")


def gql_via_http(query: str, variables: Optional[Dict] = None, attempt: int = 1) -> Dict:
    if not STORE:
        sys.exit("Set SHOPIFY_STORE (or unset SHOPIFY_TOKEN to use the CLI fallback).")
    resp = requests.post(
        ENDPOINT,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
        json={"query": query, "variables": variables or {}},
        timeout=60,
    )
    if resp.status_code == 429 and attempt <= 6:
        time.sleep(2 ** attempt)
        return gql_via_http(query, variables, attempt + 1)
    resp.raise_for_status()
    body = resp.json()
    if "errors" in body:
        if attempt <= 6:
            time.sleep(2 ** attempt)
            return gql_via_http(query, variables, attempt + 1)
        raise RuntimeError(body["errors"])
    cost = body.get("extensions", {}).get("cost", {})
    if cost.get("throttleStatus", {}).get("currentlyAvailable", 1000) < 300:
        time.sleep(1.5)
    return body["data"]


def gql_via_cli(query: str, variables: Optional[Dict] = None) -> Dict:
    query_path = var_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".graphql", delete=False, encoding="utf-8"
        ) as qf:
            qf.write(query)
            query_path = qf.name
        shopify_bin = shutil.which("shopify") or "shopify"  # resolves .cmd shims on Windows
        cmd = [shopify_bin, "store", "execute", "--store", CLI_STORE,
               "--query-file", query_path, "--json"]
        if query.strip().startswith("mutation"):
            cmd.append("--allow-mutations")
        if variables:
            with tempfile.NamedTemporaryFile(
                "w", suffix=".json", delete=False, encoding="utf-8"
            ) as vf:
                json.dump(variables, vf)
                var_path = vf.name
            cmd += ["--variable-file", var_path]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode != 0:
            raise RuntimeError(f"shopify store execute failed: {result.stderr.strip()}")
        return json.loads(result.stdout)
    finally:
        for p in (query_path, var_path):
            if p and os.path.exists(p):
                os.unlink(p)


def gql(query: str, variables: Optional[Dict] = None) -> Dict:
    """Dispatches to HTTP (SHOPIFY_TOKEN set) or the authenticated Shopify CLI (unset)."""
    if TOKEN:
        return gql_via_http(query, variables)
    return gql_via_cli(query, variables)
