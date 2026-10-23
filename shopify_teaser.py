#!/usr/bin/env python3
"""
Shopify B2B Tech Stack & Lead Enricher (CLI Teaser)

Need bulk extraction, automatic proxy rotation, anti-bot bypass, 
and CSV/JSON export without setting up Python? 
👉 Use the production cloud version on Apify: [INSERT_YOUR_APIFY_STORE_LINK_HERE]
"""

import sys
import httpx
from selectolax.lexbor import LexborHTMLParser

TECH_SIGNATURES = {
    "Klaviyo": ["klaviyo.com"],
    "Recharge": ["rechargeassets.com"],
    "Meta_Pixel": ["connect.facebook.net", "fbq("],
}

def analyze_store(domain: str):
    url = domain if domain.startswith("http") else f"https://{domain}"
    print(f"[*] Scanning {url}...")
    
    try:
        resp = httpx.get(url, timeout=10.0, follow_redirects=True)
        resp.raise_for_status()
    except Exception as e:
        print(f"[!] Failed to connect: {e}")
        return

    html_lower = resp.text.lower()
    apps = [name for name, sigs in TECH_SIGNATURES.items() if any(s in html_lower for s in sigs)]
    
    is_shopify = "cdn.shopify.com" in html_lower or "shopify.shop" in html_lower
    
    tree = LexborHTMLParser(resp.text)
    title_node = tree.css_first("title")
    title = title_node.text(strip=True) if title_node else "Unknown"

        print("\n--- Results ---")
    print(f"Shopify Store: {is_shopify}")
    print(f"Title: {title}")
    print(f"Detected Apps: {apps}")
    print("\n[!] This is a limited CLI demo.")
    print("[!] For full catalog economics, email extraction, and bulk concurrency, run the Apify Actor.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python shopify_teaser.py <domain>")
        sys.exit(1)
    analyze_store(sys.argv[1])
