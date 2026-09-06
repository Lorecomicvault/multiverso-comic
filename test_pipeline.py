import sys
from pathlib import Path

# Add local src
sys.path.append(str(Path(__file__).parent))
from src.pipeline import run_pipeline

print("English Comics Pipeline ready!")
