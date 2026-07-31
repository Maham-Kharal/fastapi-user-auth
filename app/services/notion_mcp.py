"""
Notion Live Policy Service (MCP / REST Integration)

Allows the AI Assistant to query live Notion workspace pages (e.g. Overdue Fines, Renewals, Lost Books)
directly via the Notion API before falling back to static Qdrant RAG embeddings.
"""

import logging
import httpx
from typing import Dict, Any, List, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

NOTION_SEARCH_URL = "https://api.notion.com/v1/search"
NOTION_BLOCKS_URL = "https://api.notion.com/v1/blocks/{page_id}/children"
NOTION_VERSION = "2022-06-28"


def get_notion_headers() -> Dict[str, str]:
    """Returns headers required for Notion API authentication."""
    return {
        "Authorization": f"Bearer {settings.NOTION_API_KEY}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _extract_plain_text_from_rich_text(rich_text_list: List[Dict[str, Any]]) -> str:
    """Helper to extract plain text string from Notion rich_text objects."""
    parts = []
    for pt in rich_text_list:
        if isinstance(pt, dict) and "plain_text" in pt:
            parts.append(pt["plain_text"])
    return "".join(parts)


async def get_notion_page_content(client: httpx.AsyncClient, page_id: str) -> str:
    """Fetch all block children of a Notion page and return consolidated text."""
    url = NOTION_BLOCKS_URL.format(page_id=page_id)
    headers = get_notion_headers()

    try:
        resp = await client.get(url, headers=headers, timeout=10.0)
        if resp.status_code != 200:
            logger.warning("[Notion] Failed to fetch blocks for page %s (Status: %d)", page_id, resp.status_code)
            return ""

        data = resp.json()
        blocks = data.get("results", [])
        text_lines = []

        for block in blocks:
            btype = block.get("type")
            bdata = block.get(btype, {})
            rich_text = bdata.get("rich_text", [])
            txt = _extract_plain_text_from_rich_text(rich_text)

            if not txt:
                continue

            if btype in ("heading_1", "heading_2", "heading_3"):
                text_lines.append(f"### {txt}")
            elif btype in ("bulleted_list_item", "numbered_list_item"):
                text_lines.append(f"- {txt}")
            else:
                text_lines.append(txt)

        return "\n".join(text_lines)

    except Exception as exc:
        logger.warning("[Notion] Error fetching page text for %s: %s", page_id, exc)
        return ""


async def query_notion_live_policy(query: str) -> Dict[str, Any]:
    """
    Query Notion live workspace pages for policy answers.
    Returns:
        {"found": True, "title": "...", "content": "...", "source": "Notion Live: Title"}
        or {"found": False} if Notion key is missing or no relevant page found.
    """
    if not settings.NOTION_API_KEY:
        logger.info("[Notion] NOTION_API_KEY not configured — skipping Notion live lookup.")
        return {"found": False}

    headers = get_notion_headers()
    payload = {
        "query": query,
        "filter": {"property": "object", "value": "page"},
        "page_size": 3,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(NOTION_SEARCH_URL, headers=headers, json=payload)
            if resp.status_code != 200:
                logger.warning("[Notion Search] API request failed (Status: %d)", resp.status_code)
                return {"found": False}

            data = resp.json()
            results = data.get("results", [])
            if not results:
                logger.info("[Notion Search] No Notion pages matched query: '%s'", query)
                return {"found": False}

            # Inspect matching pages for true policy content relevance
            query_terms = [w.lower() for w in query.split() if len(w) > 3]

            for page in results:
                page_id = page.get("id")
                props = page.get("properties", {})
                title_prop = props.get("title", {}) or props.get("Name", {})
                rich_title = title_prop.get("title", []) if isinstance(title_prop, dict) else []
                page_title = _extract_plain_text_from_rich_text(rich_title) or "Notion Policy Page"

                content = await get_notion_page_content(client, page_id)
                if not content or len(content.strip()) < 10:
                    continue

                # Ignore default Notion workspace onboarding templates/guides
                lower_content = content.lower()
                if "a \"view\" is a way to look at your data" in lower_content or "click done view" in lower_content:
                    logger.info("[Notion Search] Skipping default Notion tutorial page: '%s'", page_title)
                    continue

                # Check keyword relevance between query and page content/title
                title_lower = page_title.lower()
                is_relevant = any(term in title_lower or term in lower_content for term in query_terms)
                policy_keywords = ["policy", "fine", "overdue", "renew", "borrow", "fee", "lost", "loan", "book", "card", "hour", "grace"]
                has_policy_kw = any(kw in title_lower or kw in lower_content for kw in policy_keywords)

                if is_relevant or has_policy_kw:
                    logger.info("[Notion Match] Found live Notion policy: '%s' (%d chars)", page_title, len(content))
                    return {
                        "found": True,
                        "title": page_title,
                        "content": content,
                        "source": f"Notion Live: {page_title}",
                    }

            return {"found": False}

    except Exception as exc:
        logger.warning("[Notion Search] Exception during Notion lookup: %s", exc)
        return {"found": False}


async def write_notion_daily_summary(stats: dict) -> Dict[str, Any]:
    """
    Write back a daily loan/return summary entry to Notion.
    Creates a page with structured stats blocks under a 'Daily Library Reports' parent.
    """
    if not settings.NOTION_API_KEY:
        logger.warning("[Notion Write-Back] Skipping write-back: NOTION_API_KEY is not set.")
        return {"status": "skipped", "reason": "No NOTION_API_KEY"}

    yesterday_str = stats.get("yesterday", "Today")
    loans = stats.get("loans_yesterday", 0)
    returns = stats.get("returns_yesterday", 0)
    overdue = stats.get("overdue", 0)
    active = stats.get("total_active_loans", 0)
    total_books = stats.get("total_books", 0)

    headers = get_notion_headers()
    target_parent_id = settings.NOTION_DATABASE_ID.strip()
    
    # Automatically extract 32-char UUID if full Notion URL was pasted in env
    if target_parent_id and ("http" in target_parent_id or "/" in target_parent_id):
        import re
        match = re.search(r"([a-f0-9]{32})", target_parent_id.lower().replace("-", ""))
        if match:
            raw_hex = match.group(1)
            target_parent_id = f"{raw_hex[:8]}-{raw_hex[8:12]}-{raw_hex[12:16]}-{raw_hex[16:20]}-{raw_hex[20:]}"
            logger.info("[Notion Write-Back] Parsed database UUID from URL: %s", target_parent_id)

    parent_is_db = bool(target_parent_id)

    async with httpx.AsyncClient(timeout=15.0) as client:
        # Check if target_parent_id is a page containing an inline child_database
        if target_parent_id:
            try:
                page_check = await client.get(f"https://api.notion.com/v1/pages/{target_parent_id}", headers=headers)
                if page_check.status_code == 200:
                    p_obj = page_check.json().get("object")
                    if p_obj == "page":
                        # Fetch child blocks to locate the inline child_database ID
                        blocks_resp = await client.get(f"https://api.notion.com/v1/blocks/{target_parent_id}/children", headers=headers)
                        if blocks_resp.status_code == 200:
                            for b in blocks_resp.json().get("results", []):
                                if b.get("type") == "child_database":
                                    target_parent_id = b.get("id")
                                    parent_is_db = True
                                    logger.info("[Notion Write-Back] Auto-resolved child database ID: %s", target_parent_id)
                                    break
            except Exception as pe:
                logger.warning("[Notion Write-Back] Page check failed: %s", pe)
        # If database/parent page ID not explicitly provided, find or create the parent page titled 'Daily Library Reports'
        if not target_parent_id:
            try:
                search_res = await client.post(
                    NOTION_SEARCH_URL,
                    headers=headers,
                    json={"query": "Daily Library Reports", "page_size": 5},
                )
                if search_res.status_code == 200:
                    results = search_res.json().get("results", [])
                    for item in results:
                        obj_type = item.get("object")
                        props = item.get("properties", {})
                        title_prop = props.get("title", {}) or props.get("Name", {})
                        rich_title = title_prop.get("title", []) if isinstance(title_prop, dict) else []
                        page_title = _extract_plain_text_from_rich_text(rich_title)
                        if "Daily Library Reports" in page_title or obj_type == "database":
                            target_parent_id = item.get("id")
                            parent_is_db = (obj_type == "database")
                            logger.info("[Notion Write-Back] Found existing parent '%s' (ID: %s)", page_title, target_parent_id)
                            break

                # If 'Daily Library Reports' parent page does not exist yet, create it as a top-level workspace page
                if not target_parent_id:
                    logger.info("[Notion Write-Back] Creating parent page 'Daily Library Reports'...")
                    parent_resp = await client.post(
                        "https://api.notion.com/v1/pages",
                        headers=headers,
                        json={
                            "parent": {"type": "workspace", "workspace": True},
                            "properties": {
                                "title": [{"text": {"content": "Daily Library Reports"}}]
                            },
                            "children": [
                                {
                                    "object": "block",
                                    "type": "heading_1",
                                    "heading_1": {
                                        "rich_text": [{"type": "text", "text": {"content": "📁 Daily Library Reports"}}],
                                        "color": "purple_background"
                                    }
                                },
                                {
                                    "object": "block",
                                    "type": "paragraph",
                                    "paragraph": {
                                        "rich_text": [{"type": "text", "text": {"content": "Automated repository for daily library loan, return, and overdue summaries generated by ARQ background worker."}}]
                                    }
                                }
                            ]
                        }
                    )
                    if parent_resp.status_code in (200, 201):
                        parent_data = parent_resp.json()
                        target_parent_id = parent_data.get("id")
                        logger.info("[Notion Write-Back] Successfully created parent page 'Daily Library Reports' (ID: %s)", target_parent_id)
            except Exception as se:
                logger.warning("[Notion Write-Back] Search/creation for parent page failed: %s", se)

        # Build Page payload for Notion API
        title_text = f"Daily Summary - {yesterday_str}"

        # Child blocks containing daily stats breakdown
        children_blocks = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": f"📊 Daily Library Summary ({yesterday_str})"}}],
                    "color": "blue_background"
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"📚 Books Borrowed Yesterday: {loans}"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"🔄 Books Returned Yesterday: {returns}"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"⚠️ Currently Overdue Books: {overdue}"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"📖 Active Loans Balance: {active}"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"📦 Total Books in Catalog: {total_books}"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"type": "text", "text": {"content": f"Automated ARQ Background Worker Report generated on {yesterday_str}"}}],
                    "icon": {"type": "emoji", "emoji": "⚡"}
                }
            }
        ]

        if parent_is_db or (settings.NOTION_DATABASE_ID and target_parent_id == settings.NOTION_DATABASE_ID):
            parent_spec = {"database_id": target_parent_id}
            properties_spec = {
                "Name": {"title": [{"text": {"content": title_text}}]},
                "Date": {"date": {"start": yesterday_str}},
                "Loans": {"number": loans},
                "Returns": {"number": returns},
                "Overdue": {"number": overdue},
            }
        elif target_parent_id:
            parent_spec = {"page_id": target_parent_id}
            properties_spec = {
                "title": [{"text": {"content": title_text}}]
            }
        else:
            parent_spec = {"type": "workspace", "workspace": True}
            properties_spec = {
                "title": [{"text": {"content": title_text}}]
            }

        create_payload = {
            "parent": parent_spec,
            "properties": properties_spec,
            "children": children_blocks,
        }

        try:
            resp = await client.post("https://api.notion.com/v1/pages", headers=headers, json=create_payload)
            if resp.status_code in (200, 201):
                page_data = resp.json()
                page_id = page_data.get("id")
                page_url = page_data.get("url")
                logger.info("[Notion Write-Back SUCCESS] Created Notion summary page: '%s' (ID: %s, URL: %s)", title_text, page_id, page_url)
                return {
                    "status": "success",
                    "page_id": page_id,
                    "url": page_url,
                    "title": title_text,
                }
            else:
                logger.error("[Notion Write-Back ERROR] HTTP %d: %s", resp.status_code, resp.text)
                return {"status": "failed", "status_code": resp.status_code, "error": resp.text}

        except Exception as exc:
            logger.error("[Notion Write-Back Exception] %s", exc)
            return {"status": "failed", "error": str(exc)}

