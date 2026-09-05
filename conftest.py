import os
import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent
AI_DIR = ROOT_DIR / "tbk-spfy-ai"
SEO_DIR = ROOT_DIR / "tbk-spfy-seo" / "ops"

# Ensure sys.path includes all submodules
for p in (AI_DIR, SEO_DIR, ROOT_DIR):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)


@pytest.fixture(autouse=True, scope="session")
def setup_test_environment():
    """Set working directory to tbk-spfy-ai so relative paths inside AI tests resolve cleanly."""
    orig_cwd = os.getcwd()
    if AI_DIR.exists():
        os.chdir(AI_DIR)
    yield
    os.chdir(orig_cwd)

