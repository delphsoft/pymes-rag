"""
pipeline.py — Pymes Studio RAG Pipeline
Orchestrates: crawl → judge → questions → store

Usage:
  python pipeline.py                    # full run, fallback judge (no API key)
  python pipeline.py --api-key sk-...   # full run with Claude judge
  python pipeline.py --source arca      # only crawl ARCA
  python pipeline.py --source bora      # only crawl BORA
  python pipeline.py --dry-run          # crawl only, no judge/store
"""
import argparse
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from crawler.arca import crawl_all_arca
from crawler.bora import crawl_all_bora
from judge.quality_scorer import judge_batch
from processor.questions import add_questions_batch
from storage.store import save_batch, print_summary


def run_pipeline(source: str = "all", api_key: str | None = None,
                 dry_run: bool = False):
    start = datetime.utcnow()
    print(f"\n{'='*50}")
    print(f"Pymes Studio RAG Pipeline — {start.strftime('%Y-%m-%d %H:%M')} UTC")
    print(f"Source: {source} | Judge: {'Claude API' if api_key else 'Fallback'}")
    print(f"{'='*50}\n")

    # ── Step 1: Crawl
    all_chunks = []

    if source in ("all", "arca"):
        print("[1/4] Crawling ARCA...")
        arca_chunks = crawl_all_arca()
        all_chunks.extend(arca_chunks)

    if source in ("all", "bora"):
        print("[1/4] Crawling BORA...")
        bora_chunks = crawl_all_bora()
        all_chunks.extend(bora_chunks)

    print(f"\nTotal chunks crawled: {len(all_chunks)}")

    if dry_run:
        print("\n[DRY RUN] Stopping after crawl.")
        for c in all_chunks[:3]:
            print(f"  - {c.source_name}: {c.content_clean[:100]}...")
        return

    if not all_chunks:
        print("[ERROR] No chunks crawled. Check network access.")
        return

    # ── Step 2: Judge quality
    print(f"\n[2/4] Judging {len(all_chunks)} chunks...")
    stats = judge_batch(all_chunks, api_key=api_key, verbose=True)
    print(f"  Results: {stats}")

    # ── Step 3: Generate synthetic questions (accepted only)
    print(f"\n[3/4] Generating synthetic questions...")
    all_chunks = add_questions_batch(all_chunks, api_key=api_key, only_accepted=True)

    # ── Step 4: Save
    print(f"\n[4/4] Saving to local storage...")
    save_batch(all_chunks, verbose=True)

    # ── Summary
    print_summary(all_chunks)

    elapsed = (datetime.utcnow() - start).seconds
    print(f"\nTotal time: {elapsed}s")

    return all_chunks


def main():
    parser = argparse.ArgumentParser(description="Pymes Studio RAG Pipeline")
    parser.add_argument("--source", choices=["all", "arca", "bora"],
                        default="all", help="Data source to crawl")
    parser.add_argument("--api-key", default=os.getenv("ANTHROPIC_API_KEY"),
                        help="Anthropic API key for Claude judge")
    parser.add_argument("--dry-run", action="store_true",
                        help="Crawl only, skip judge and store")
    args = parser.parse_args()

    run_pipeline(
        source=args.source,
        api_key=args.api_key,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
