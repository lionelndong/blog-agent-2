#!/usr/bin/env python3
"""Build the keyword queue from DataForSEO.

This is intentionally small and explicit: it smoke-tests the mapped endpoints,
logs provider cost, builds a candidate pool, applies deterministic BID/AIO
gates, and writes keyword-ideas.csv + keyword-queue.csv.
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
KEYWORD_DIR = ROOT / "content-pipeline" / "0-keywords"
CACHE_DIR = KEYWORD_DIR / "cache"
ARTIFACT_DIR = ROOT.parents[0] / "artifacts" / "PLE-1330"
BASE_URL = "https://api.dataforseo.com/v3"
LOCATION_CODE = 2840
LANGUAGE_CODE = "en"
BRAND_DOMAIN = "pleasur.ai"
KNOWN_COMPETITORS = ["candy.ai", "ourdream.ai", "nastia.ai"]
GENERIC_COMPETITOR_DOMAINS = {
    "reddit.com",
    "youtube.com",
    "google.com",
    "instagram.com",
    "facebook.com",
    "x.com",
    "twitter.com",
    "tiktok.com",
    "wikipedia.org",
    "amazon.com",
}

ENDPOINTS = {
    "keyword_overview": "/dataforseo_labs/google/keyword_overview/live",
    "keyword_suggestions": "/dataforseo_labs/google/keyword_suggestions/live",
    "keyword_ideas": "/dataforseo_labs/google/keyword_ideas/live",
    "competitors_domain": "/dataforseo_labs/google/competitors_domain/live",
    "domain_intersection": "/dataforseo_labs/google/domain_intersection/live",
    "serp_advanced": "/serp/google/organic/live/advanced",
}

SEEDS = [
    "ai girlfriend",
    "ai companion",
    "nsfw ai chat",
    "ai sexting",
    "ai boyfriend",
    "ai roleplay",
    "nsfw ai image generator",
    "uncensored ai chat",
]

QUESTION_PREFIXES = (
    "who ",
    "what ",
    "when ",
    "where ",
    "why ",
    "how ",
    "can ",
    "does ",
    "do ",
    "is ",
    "are ",
    "best ",
    "free ",
)

LOW_FIT_TERMS = (
    "candy ai",
    "candy.ai",
    "ourdream",
    "nastia",
    "spicychat",
    "replika",
    "muah",
    "perchance",
    "character.ai",
    "movie",
    "robot",
)

HIGH_FIT_TERMS = (
    "ai girlfriend",
    "ai boyfriend",
    "ai companion",
    "ai roleplay",
    "ai sext",
    "sexting",
    "sex chat",
    "nsfw chat",
    "nsfw ai",
    "uncensored ai",
    "virtual girlfriend",
    "ai gf",
    "ai bf",
    "dirty talk",
    "horny ai",
    "romantic ai",
    "ai character",
    "naughty ai",
)

IMAGE_TERMS = (
    "image generator",
    "ai image",
    "nsfw image",
    "ai picture",
    "ai photo",
    "ai art",
    "porn generator",
)


@dataclass
class ApiResult:
    endpoint_key: str
    endpoint: str
    status_code: int
    cost: float
    response: dict[str, Any]


class DataForSeoClient:
    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run
        self.calls: list[dict[str, Any]] = []
        self.auth = self._auth_header()
        if not self.auth and not dry_run:
            raise SystemExit(
                "Missing DataForSEO credentials. Run through Doppler with "
                "DATAFORSEO_LOGIN/DATAFORSEO_PASSWORD or DATAFORSEO_API_KEY_BASE64."
            )

    @staticmethod
    def _auth_header() -> str | None:
        login = os.environ.get("DATAFORSEO_LOGIN") or os.environ.get("DATAFORSEO_USERNAME")
        password = os.environ.get("DATAFORSEO_PASSWORD")
        if login and password:
            token = base64.b64encode(f"{login}:{password}".encode()).decode()
            return "Basic " + token
        if os.environ.get("DATAFORSEO_API_KEY_BASE64"):
            return "Basic " + os.environ["DATAFORSEO_API_KEY_BASE64"]
        return None

    def post(self, endpoint_key: str, payload: list[dict[str, Any]]) -> ApiResult:
        endpoint = ENDPOINTS[endpoint_key]
        if self.dry_run:
            result = ApiResult(endpoint_key, endpoint, 0, 0.0, {"tasks": []})
            self._log_call(result, len(payload))
            return result

        body = json.dumps(payload).encode()
        request = urllib.request.Request(
            BASE_URL + endpoint,
            data=body,
            method="POST",
            headers={
                "Authorization": self.auth or "",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                raw = response.read().decode()
                data = json.loads(raw) if raw else {}
                status = response.status
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode(errors="replace")
            data = json.loads(raw) if raw.startswith("{") else {"error": raw[:500]}
            status = exc.code

        tasks = data.get("tasks") if isinstance(data.get("tasks"), list) else []
        cost = sum(float(task.get("cost") or 0) for task in tasks)
        result = ApiResult(endpoint_key, endpoint, status, cost, data)
        self._log_call(result, len(payload))
        return result

    def _log_call(self, result: ApiResult, task_count: int) -> None:
        entry = {
            "observed_at": utc_now(),
            "provider": "DataForSEO",
            "endpoint_key": result.endpoint_key,
            "endpoint": result.endpoint,
            "status_code": result.status_code,
            "task_count": task_count,
            "cost_usd": round(result.cost, 6),
        }
        self.calls.append(entry)

    @property
    def total_cost(self) -> float:
        return sum(float(call["cost_usd"]) for call in self.calls)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def observed_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def task_results(response: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for task in response.get("tasks", []) or []:
        for result in task.get("result") or []:
            if isinstance(result, dict):
                out.append(result)
    return out


def result_items(response: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for result in task_results(response):
        items = result.get("items")
        if isinstance(items, list):
            out.extend(item for item in items if isinstance(item, dict))
        elif result:
            out.append(result)
    return out


def nested(obj: dict[str, Any], *path: str, default: Any = None) -> Any:
    cur: Any = obj
    for part in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(part)
    return cur if cur is not None else default


def normalize_keyword_item(item: dict[str, Any], source: str, gap_mode: str) -> dict[str, Any] | None:
    keyword = (
        item.get("keyword")
        or nested(item, "keyword_data", "keyword")
        or nested(item, "keyword_info", "keyword")
    )
    if not keyword:
        return None

    keyword_info = item.get("keyword_info") or nested(item, "keyword_data", "keyword_info", default={}) or {}
    keyword_props = item.get("keyword_properties") or nested(item, "keyword_data", "keyword_properties", default={}) or {}
    intent = item.get("search_intent_info") or nested(item, "keyword_data", "search_intent_info", default={}) or {}
    serp_info = item.get("serp_info") or nested(item, "keyword_data", "serp_info", default={}) or {}

    kd = (
        keyword_props.get("keyword_difficulty")
        or item.get("keyword_difficulty")
        or nested(item, "keyword_data", "keyword_properties", "keyword_difficulty")
    )
    volume = keyword_info.get("search_volume") or item.get("search_volume") or 0
    cpc = keyword_info.get("cpc") or item.get("cpc") or 0
    traffic_potential = (
        serp_info.get("se_results_count")
        or item.get("traffic")
        or item.get("etv")
        or volume
        or 0
    )

    return {
        "keyword": clean_keyword(str(keyword)),
        "volume": int_or_zero(volume),
        "kd": int_or_zero(kd),
        "traffic_potential": int_or_zero(traffic_potential),
        "cpc": float_or_zero(cpc),
        "source": source,
        "gap_mode": gap_mode,
        "intent": dominant_intent(intent),
        "search_intent_info": json.dumps(intent, sort_keys=True) if intent else "",
        "competitor_top_position": item.get("rank_absolute") or nested(item, "first_domain_serp_element", "rank_absolute", default=""),
        "competitor_domains": item.get("domain") or nested(item, "first_domain_serp_element", "domain", default=""),
        "parent_topic": "",
        "serp_features": "",
    }


def clean_keyword(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def int_or_zero(value: Any) -> int:
    try:
        if value is None or value == "":
            return 0
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def float_or_zero(value: Any) -> float:
    try:
        if value is None or value == "":
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def dominant_intent(intent: Any) -> str:
    if not isinstance(intent, dict):
        return ""
    label = intent.get("main_intent") or intent.get("intent")
    if label:
        return str(label)
    probabilities = intent.get("probabilities") or intent.get("intent_probabilities") or {}
    if isinstance(probabilities, dict) and probabilities:
        return str(max(probabilities.items(), key=lambda item: float_or_zero(item[1]))[0])
    for name in ("informational", "commercial", "transactional", "navigational"):
        if float_or_zero(intent.get(name)) > 0:
            return name
    return ""


def slugify(keyword: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", keyword.lower()).strip("-")
    return slug or "keyword"


def brand_fit(keyword: str) -> int:
    kl = keyword.lower()
    if any(term in kl for term in LOW_FIT_TERMS):
        return 3
    if any(term in kl for term in HIGH_FIT_TERMS):
        return 9
    if any(term in kl for term in IMAGE_TERMS):
        return 8
    if "ai" in kl and any(term in kl for term in ("girl", "boy", "companion", "chat", "sex", "nsfw", "adult", "roleplay")):
        return 7
    if "ai" in kl:
        return 5
    return 2


def product_fit(keyword: str) -> int:
    kl = keyword.lower()
    creator = any(term in kl for term in ("girlfriend", "boyfriend", "companion", "chat", "roleplay", "sext", "character", "dirty talk"))
    image = any(term in kl for term in IMAGE_TERMS)
    if creator and image:
        return 9
    if creator:
        return 8
    if image:
        return 7
    if "ai" in kl and any(term in kl for term in ("adult", "nsfw", "sex")):
        return 6
    return 3


def classify_intent(keyword: str, dataforseo_intent: str, serp_items: list[dict[str, Any]]) -> str:
    kl = keyword.lower()
    if tool_led(keyword, serp_items):
        return "tool-led"
    if dataforseo_intent in {"informational", "commercial"}:
        if any(token in kl for token in ("best ", " vs ", "review", "alternative", " app", " apps")):
            return "commercial-investigation"
        return dataforseo_intent
    if dataforseo_intent in {"transactional", "navigational"}:
        return dataforseo_intent
    if any(token in kl for token in ("best ", " vs ", "review", "alternative")):
        return "commercial-investigation"
    return "informational"


def tool_led(keyword: str, serp_items: list[dict[str, Any]]) -> bool:
    kl = keyword.lower()
    if any(token in kl for token in ("generator", "creator", "maker", "tool", "calculator")) and not kl.startswith("best "):
        return True
    hits = 0
    for item in serp_items[:5]:
        text = f"{item.get('title','')} {item.get('url','')}".lower()
        if any(token in text for token in ("/tools/", "/tool/", "/generator", "/calculator", "free tool")):
            hits += 1
    return hits >= 3


def weak_link_count(serp_items: list[dict[str, Any]]) -> int:
    weak_domains = ("reddit.com", "quora.com", "medium.com", "github.io", "wordpress.com", "blogspot.com")
    count = 0
    for item in serp_items[:10]:
        text = f"{item.get('domain','')} {item.get('url','')} {item.get('title','')}".lower()
        if any(domain in text for domain in weak_domains):
            count += 1
        elif any(token in text for token in ("/blog/", "/best-", "/guide", "top 10", "list")):
            count += 1
    return count


def traffic_score(traffic_potential: int, kd: int) -> float:
    raw = min(10.0, math.log10(max(traffic_potential, 0) + 1) * 2) - (kd / 20.0)
    return max(0.0, min(10.0, raw))


def priority_score(row: dict[str, Any]) -> tuple[float, str]:
    base = 0.4 * traffic_score(row["traffic_potential"], row["kd"]) + 0.3 * row["brand_fit"] + 0.3 * row["product_fit"]
    boost = 0.0
    if row["gap_mode"] == "missing":
        boost += 0.4
    elif row["gap_mode"] == "weak":
        boost += 0.5
    elif row["gap_mode"] == "question_mining":
        boost += 0.3
    if row["serp_intent"] == "tool-led":
        boost += 1.0
    score = base + boost
    notes = f"base={base:.2f} (T={traffic_score(row['traffic_potential'], row['kd']):.2f},BF={row['brand_fit']},PF={row['product_fit']}) boost={boost:.1f}"
    return score, notes


def dedupe_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best: dict[str, dict[str, Any]] = {}
    source_priority = {"missing": 5, "weak": 4, "question_mining": 3, "seed_modifier": 2}
    for row in candidates:
        keyword = row["keyword"]
        if not keyword or len(keyword) < 3:
            continue
        if any(term in keyword for term in LOW_FIT_TERMS):
            continue
        existing = best.get(keyword)
        if not existing:
            best[keyword] = row
            continue
        if source_priority.get(row.get("gap_mode", ""), 0) > source_priority.get(existing.get("gap_mode", ""), 0):
            row["source"] = merge_source(existing["source"], row["source"])
            best[keyword] = row
        else:
            existing["source"] = merge_source(existing["source"], row["source"])
            existing["traffic_potential"] = max(existing["traffic_potential"], row["traffic_potential"])
            existing["volume"] = max(existing["volume"], row["volume"])
            if not existing.get("intent") and row.get("intent"):
                existing["intent"] = row["intent"]
    return list(best.values())


def merge_source(left: str, right: str) -> str:
    parts = sorted(set(filter(None, left.split("+") + right.split("+"))))
    return "+".join(parts)


def smoke_test(client: DataForSeoClient) -> dict[str, Any]:
    smoke_payloads = {
        "keyword_overview": [{"keywords": ["ai girlfriend"], "location_code": LOCATION_CODE, "language_code": LANGUAGE_CODE, "limit": 1}],
        "keyword_suggestions": [{"keyword": "ai girlfriend", "location_code": LOCATION_CODE, "language_code": LANGUAGE_CODE, "limit": 1}],
        "keyword_ideas": [{"keywords": ["ai girlfriend"], "location_code": LOCATION_CODE, "language_code": LANGUAGE_CODE, "limit": 1}],
        "competitors_domain": [{"target": BRAND_DOMAIN, "location_code": LOCATION_CODE, "language_code": LANGUAGE_CODE, "limit": 1}],
        "domain_intersection": [{"target1": "candy.ai", "target2": BRAND_DOMAIN, "location_code": LOCATION_CODE, "language_code": LANGUAGE_CODE, "intersections": False, "limit": 1}],
        "serp_advanced": [{"keyword": "ai girlfriend", "location_code": LOCATION_CODE, "language_code": LANGUAGE_CODE, "device": "desktop", "os": "windows", "depth": 10}],
    }
    results: dict[str, Any] = {"observed_at": utc_now(), "location_code": LOCATION_CODE, "language_code": LANGUAGE_CODE, "endpoints": []}
    for key, payload in smoke_payloads.items():
        before = len(client.calls)
        response = client.post(key, payload)
        fields = observed_fields(key, response.response)
        call = client.calls[before]
        results["endpoints"].append({**call, "observed_fields": fields})
        time.sleep(0.25)
    return results


def observed_fields(key: str, response: dict[str, Any]) -> list[str]:
    if key == "serp_advanced":
        items = result_items(response)
        types = sorted(set(str(item.get("type")) for item in items if item.get("type")))
        return ["items.type=" + ",".join(types[:8])]
    items = result_items(response)
    if not items:
        return []
    first = items[0]
    fields = sorted(first.keys())[:12]
    nested_fields = []
    for parent in ("keyword_info", "keyword_properties", "search_intent_info", "keyword_data"):
        if isinstance(first.get(parent), dict):
            nested_fields.append(parent + "." + ",".join(sorted(first[parent].keys())[:6]))
    return fields + nested_fields


def collect_candidates(client: DataForSeoClient, per_seed_limit: int) -> tuple[list[dict[str, Any]], list[str]]:
    candidates: list[dict[str, Any]] = []
    competitors: list[str] = []

    comp_response = client.post("competitors_domain", [{"target": BRAND_DOMAIN, "location_code": LOCATION_CODE, "language_code": LANGUAGE_CODE, "limit": 5}])
    for item in result_items(comp_response.response):
        domain = item.get("domain") or item.get("target")
        if domain and domain != BRAND_DOMAIN:
            normalized = str(domain).replace("www.", "")
            if normalized not in GENERIC_COMPETITOR_DOMAINS:
                competitors.append(normalized)
    if len(competitors) < 2:
        competitors = KNOWN_COMPETITORS
    competitors = competitors[:3]

    for competitor in competitors:
        payload = [{
            "target1": competitor,
            "target2": BRAND_DOMAIN,
            "location_code": LOCATION_CODE,
            "language_code": LANGUAGE_CODE,
            "intersections": False,
            "limit": 30,
        }]
        response = client.post("domain_intersection", payload)
        for item in result_items(response.response):
            row = normalize_keyword_item(item, "competitor_gap", "missing")
            if row:
                row["competitor_domains"] = competitor
                candidates.append(row)

    for seed in SEEDS:
        suggestions = client.post("keyword_suggestions", [{"keyword": seed, "location_code": LOCATION_CODE, "language_code": LANGUAGE_CODE, "limit": per_seed_limit}])
        for item in result_items(suggestions.response):
            row = normalize_keyword_item(item, "seed_modifier", "seed_modifier")
            if row:
                candidates.append(row)
                if row["keyword"].startswith(QUESTION_PREFIXES) or "?" in row["keyword"]:
                    qrow = dict(row)
                    qrow["source"] = merge_source(qrow["source"], "question_mining")
                    qrow["gap_mode"] = "question_mining"
                    candidates.append(qrow)

        ideas = client.post("keyword_ideas", [{"keywords": [seed], "location_code": LOCATION_CODE, "language_code": LANGUAGE_CODE, "limit": per_seed_limit}])
        for item in result_items(ideas.response):
            row = normalize_keyword_item(item, "seed_modifier", "seed_modifier")
            if row:
                candidates.append(row)

    return dedupe_candidates(candidates), competitors


def enrich_overview(client: DataForSeoClient, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_keyword = {row["keyword"]: row for row in candidates}
    keywords = list(by_keyword.keys())
    for chunk in chunks(keywords, 100):
        response = client.post("keyword_overview", [{"keywords": chunk, "location_code": LOCATION_CODE, "language_code": LANGUAGE_CODE}])
        for item in result_items(response.response):
            row = normalize_keyword_item(item, "overview", by_keyword.get(clean_keyword(str(item.get("keyword") or nested(item, "keyword_data", "keyword", default=""))), {}).get("gap_mode", "seed_modifier"))
            if not row:
                continue
            target = by_keyword.get(row["keyword"])
            if not target:
                continue
            for field in ("volume", "kd", "traffic_potential", "cpc", "intent", "search_intent_info"):
                if row.get(field):
                    target[field] = row[field]
    return list(by_keyword.values())


def chunks(items: list[Any], size: int) -> list[list[Any]]:
    return [items[index:index + size] for index in range(0, len(items), size)]


def collect_serp(client: DataForSeoClient, candidates: list[dict[str, Any]], limit: int) -> dict[str, list[dict[str, Any]]]:
    selected = sorted(
        candidates,
        key=lambda row: (
            brand_fit(row["keyword"]),
            product_fit(row["keyword"]),
            row["volume"],
            row["traffic_potential"],
        ),
        reverse=True,
    )[:limit]
    serp_by_keyword: dict[str, list[dict[str, Any]]] = {}
    for index, row in enumerate(selected, start=1):
        if index == 1 or index % 10 == 0 or index == len(selected):
            print(f"[dataforseo] SERP check {index}/{len(selected)}", file=sys.stderr, flush=True)
        requested_keyword = row["keyword"]
        # DataForSEO live SERP Advanced accepts only one task per POST. Additional
        # tasks are returned as 40000 "You can set only one task at a time."
        payload = [
            {"keyword": requested_keyword, "location_code": LOCATION_CODE, "language_code": LANGUAGE_CODE, "device": "desktop", "os": "windows", "depth": 20}
        ]
        response = client.post("serp_advanced", payload)
        for task in response.response.get("tasks", []) or []:
            task_keyword = nested(task, "data", "keyword", default="")
            for result in task.get("result") or []:
                if not isinstance(result, dict):
                    continue
                keyword = clean_keyword(str(result.get("keyword") or task_keyword or requested_keyword))
                items = result.get("items") if isinstance(result.get("items"), list) else []
                if keyword:
                    serp_by_keyword[keyword] = items
        if requested_keyword not in serp_by_keyword:
            serp_by_keyword[requested_keyword] = []
    return serp_by_keyword


def vet_and_score(candidates: list[dict[str, Any]], serp: dict[str, list[dict[str, Any]]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    ideas: list[dict[str, Any]] = []
    for row in candidates:
        items = serp.get(row["keyword"], [])
        row["serp_features"] = ",".join(sorted(set(str(item.get("type")) for item in items if item.get("type"))))
        row["has_aio"] = "true" if any(item.get("type") == "ai_overview" for item in items) else "false"
        row["aio_body_source"] = "serp_advanced" if items else "not_checked"
        row["aio_completeness_score"] = 4 if row["has_aio"] == "true" else ""
        row["aio_click_intent"] = "unknown" if row["has_aio"] == "true" else ""
        row["aio_verdict"] = "RISKY" if row["has_aio"] == "true" else ("PASS" if items else "UNKNOWN")
        row["aio_reasoning"] = "DataForSEO SERP Advanced returned ai_overview item." if row["has_aio"] == "true" else ("No ai_overview item in observed SERP." if items else "SERP not checked in this budgeted run.")
        row["brand_fit"] = brand_fit(row["keyword"])
        row["product_fit"] = product_fit(row["keyword"])
        row["serp_intent"] = classify_intent(row["keyword"], row.get("intent", ""), items)
        row["weak_link_count"] = weak_link_count(items)
        row["weak_link_count_source"] = "serp_shape" if items else "not_checked"
        row["bid_verdict"], row["bid_reason"] = bid_verdict(row)
        row["redteam_verdict"] = "KEEP" if row["bid_verdict"] == "PASS" and row["aio_verdict"] in {"PASS", "RISKY"} else "DROP"
        row["redteam_priority_delta"] = "0"
        row["redteam_critique_summary"] = "Deterministic DataForSEO migration run; manual adversarial review still required before article production." if row["redteam_verdict"] == "KEEP" else row["bid_reason"] or row["aio_verdict"]
        score, notes = priority_score(row)
        row["priority_score"] = round(score, 2)
        row["notes"] = notes
        ideas.append(row)

    survivors = [row for row in ideas if row["bid_verdict"] == "PASS" and row["aio_verdict"] in {"PASS", "RISKY"} and row["serp_intent"] != "tool-led"]
    survivors.sort(key=lambda row: (row["priority_score"], row["volume"], row["traffic_potential"]), reverse=True)
    for rank, row in enumerate(survivors[:50], start=1):
        row["rank"] = rank
        row["slug"] = slugify(row["keyword"])
    return ideas, survivors[:50]


def bid_verdict(row: dict[str, Any]) -> tuple[str, str]:
    if row["brand_fit"] < 4:
        return "FAIL", "low_brand_fit"
    if row["product_fit"] < 3:
        return "FAIL", "low_product_fit"
    if row["serp_intent"] == "transactional":
        return "FAIL", "serp_is_transactional"
    if row["serp_intent"] == "navigational":
        return "FAIL", "serp_is_navigational"
    if row["kd"] and row["kd"] > 70 and not (row["brand_fit"] >= 8 and row["product_fit"] >= 7 and row["kd"] <= 85):
        return "FAIL", "dataforseo_kd_too_high"
    if row["has_aio"] == "true" and row["serp_intent"] == "informational" and row["volume"] < 100:
        return "FAIL", "aio_low_click_risk"
    return "PASS", ""


def write_outputs(smoke: dict[str, Any], ideas: list[dict[str, Any]], queue: list[dict[str, Any]], competitors: list[str], client: DataForSeoClient) -> None:
    KEYWORD_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    idea_fields = [
        "keyword", "volume", "kd", "traffic_potential", "cpc", "competitor_top_position", "competitor_domains",
        "parent_topic", "intent", "search_intent_info", "source", "gap_mode", "serp_features", "brand_fit",
        "product_fit", "serp_intent", "weak_link_count", "weak_link_count_source", "bid_verdict", "bid_reason",
        "has_aio", "aio_completeness_score", "aio_click_intent", "aio_verdict", "aio_reasoning", "aio_body_source",
        "redteam_verdict", "redteam_priority_delta", "redteam_critique_summary", "priority_score", "notes",
    ]
    with (KEYWORD_DIR / "keyword-ideas.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=idea_fields)
        writer.writeheader()
        for row in ideas:
            writer.writerow({field: row.get(field, "") for field in idea_fields})

    queue_fields = [
        "rank", "keyword", "slug", "priority_score", "volume", "kd", "traffic_potential", "source", "gap_mode",
        "serp_intent", "bid_verdict", "aio_verdict", "redteam_verdict", "brand_fit", "product_fit",
        "competitor_top_position", "competitor_domains", "parent_topic", "intent", "redteam_priority_delta",
        "redteam_critique_summary", "notes",
    ]
    with (KEYWORD_DIR / "keyword-queue.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=queue_fields)
        writer.writeheader()
        for row in queue:
            writer.writerow({field: row.get(field, "") for field in queue_fields})

    tool_rows = [row for row in ideas if row.get("serp_intent") == "tool-led" and row.get("bid_verdict") == "PASS"]
    with (KEYWORD_DIR / "tool-opportunities.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=queue_fields[1:])
        writer.writeheader()
        for row in sorted(tool_rows, key=lambda item: item["priority_score"], reverse=True):
            writer.writerow({field: row.get(field, "") for field in queue_fields[1:]})

    smoke["total_cost_usd"] = round(sum(item["cost_usd"] for item in smoke["endpoints"]), 6)
    smoke["run_total_cost_usd"] = round(client.total_cost, 6)
    smoke_path = CACHE_DIR / "dataforseo-smoke-results.json"
    smoke_path.write_text(json.dumps(smoke, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (ARTIFACT_DIR / "dataforseo-smoke-results.json").write_text(smoke_path.read_text(encoding="utf-8"), encoding="utf-8")

    run_summary = render_summary(ideas, queue, competitors, client)
    (KEYWORD_DIR / "dataforseo-run-summary.md").write_text(run_summary, encoding="utf-8")
    (ARTIFACT_DIR / "dataforseo-run-summary.md").write_text(run_summary, encoding="utf-8")


def render_summary(ideas: list[dict[str, Any]], queue: list[dict[str, Any]], competitors: list[str], client: DataForSeoClient) -> str:
    source_counts = Counter(row["source"] for row in ideas)
    gap_counts = Counter(row["gap_mode"] for row in ideas)
    bid_counts = Counter(row["bid_verdict"] for row in ideas)
    aio_counts = Counter(row["aio_verdict"] for row in ideas)
    lines = [
        "# DataForSEO Keyword Research Run",
        "",
        f"- Observed date: {observed_date()}",
        f"- Source: DataForSEO API v3, US Google (`location_code={LOCATION_CODE}`, `language_code={LANGUAGE_CODE}`)",
        f"- Cost logged: ${client.total_cost:.6f}",
        f"- Competitors used: {', '.join(competitors)}",
        f"- Candidate rows: {len(ideas)}",
        f"- Queue rows: {len(queue)}",
        f"- Source counts: {dict(source_counts)}",
        f"- Gap-mode counts: {dict(gap_counts)}",
        f"- BID counts: {dict(bid_counts)}",
        f"- AIO counts: {dict(aio_counts)}",
        "",
        "## Top 10 Queue Rows",
        "",
        "| Rank | Keyword | Score | Volume | KD | Intent | Source | Gap |",
        "|---:|---|---:|---:|---:|---|---|---|",
    ]
    for row in queue[:10]:
        lines.append(
            f"| {row['rank']} | {row['keyword']} | {row['priority_score']:.2f} | {row['volume']} | {row['kd']} | {row['serp_intent']} | {row['source']} | {row['gap_mode']} |"
        )
    lines.extend([
        "",
        "## Caveats",
        "",
        "- Lens: Search intent alignment. DataForSEO `search_intent_info` is primary when available; SERP shape is fallback.",
        "- Lens: Answer-engine citation readiness. AIO detection uses SERP Advanced `ai_overview`; multi-engine LLM citation gap is skipped because DataForSEO has no equivalent.",
        "- Lens: E-E-A-T. This queue is mechanically vetted; article production still requires the normal research, quality, claim verification, and compliance gates.",
    ])
    return "\n".join(lines) + "\n"


def validate_queue() -> None:
    path = KEYWORD_DIR / "keyword-queue.csv"
    with path.open("r", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 50:
        raise SystemExit(f"keyword-queue.csv has {len(rows)} rows; expected 50")
    required = {"rank", "keyword", "slug", "priority_score", "volume", "kd", "source", "gap_mode", "bid_verdict", "aio_verdict"}
    missing = required - set(rows[0])
    if missing:
        raise SystemExit(f"keyword-queue.csv missing columns: {sorted(missing)}")
    print(f"Validated keyword-queue.csv: {len(rows)} rows, top keyword={rows[0]['keyword']!r}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-seed-limit", type=int, default=35)
    parser.add_argument("--serp-limit", type=int, default=80)
    parser.add_argument("--smoke-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.dry_run and not args.smoke_only:
        print("Dry run only validates credential-free startup. Use --smoke-only for endpoint checks.")
        return 0
    client = DataForSeoClient(dry_run=args.dry_run)
    smoke = smoke_test(client)
    if args.smoke_only:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        (CACHE_DIR / "dataforseo-smoke-results.json").write_text(json.dumps(smoke, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"smoke_cost_usd": round(client.total_cost, 6), "endpoints": [item["endpoint_key"] for item in client.calls]}, indent=2))
        return 0

    print("[dataforseo] collecting candidate pool", file=sys.stderr, flush=True)
    candidates, competitors = collect_candidates(client, args.per_seed_limit)
    print(f"[dataforseo] collected {len(candidates)} deduped candidates", file=sys.stderr, flush=True)
    print("[dataforseo] enriching keyword overview", file=sys.stderr, flush=True)
    candidates = enrich_overview(client, candidates)
    print(f"[dataforseo] collecting live SERP for top {args.serp_limit}", file=sys.stderr, flush=True)
    serp = collect_serp(client, candidates, args.serp_limit)
    print("[dataforseo] vetting and scoring", file=sys.stderr, flush=True)
    ideas, queue = vet_and_score(candidates, serp)
    write_outputs(smoke, ideas, queue, competitors, client)
    validate_queue()
    print(f"DataForSEO run complete: candidates={len(ideas)} queue={len(queue)} cost=${client.total_cost:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
