import os
import webbrowser
from pathlib import Path


if __name__ == "__main__":
    webbrowser.open(Path(os.path.join(os.path.dirname(__file__), "index.html")).resolve().as_uri())
