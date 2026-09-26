"""
Trade API Tester
Interactive UI Entry Point.
"""
import sys
from pathlib import Path

# Allow project-local libraries

env = sys.argv[1] if len(sys.argv) > 1 else "prod"

if not env == "dev":
   ROOT = Path(__file__).parent
   LIBS = ROOT / "libs"
   if LIBS.exists():
      sys.path.insert(0, str(LIBS))

from ui.app import ApiTesterApp

def main():
   app = ApiTesterApp()
   app.run()

if __name__ == "__main__":
   main()