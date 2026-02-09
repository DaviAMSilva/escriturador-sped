import webbrowser
from pathlib import Path


if __name__ == "__main__":
    webbrowser.open((Path(__file__).parent / "index.html").resolve().as_uri())
