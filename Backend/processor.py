from fastapi import FastAPI, HTTPException, Request
import asyncio
import os
from scrapers.scraper_orchestrator import main as run_scrapers
from utils import load_env