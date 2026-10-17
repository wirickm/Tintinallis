"""Paths and settings shared across the pipeline."""

from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
SUMMARY_DIR = DATA_DIR / "summaries"
DB_DIR = ROOT / "vector_db"
CHAT_LOG = DATA_DIR / "chat_log.csv"

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = (
    "You are an assistant that analyzes the contents of an emergency medicine book "
    "please do not summarize, instead, retain as much relevant text as possible, ignoring text that might be chapter or section related. "
)
