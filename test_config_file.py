import tempfile
from pathlib import Path

from config_parser import ConfigError, load_config

BASE = {
    "WIDTH": "20",
    "HEIGHT": "15",
    "ENTRY": "0,0",
    "EXIT": "19,14",
    "OUTPUT_FILE": "maze.txt",
    "PERFECT": "True",
}


def make_text(**changes: str) -> str:
    """Build a config text from BASE. A value of None removes the key."""
    data = {**BASE, **changes}
    return "\n".join(f"{k}={v}" for k, v in data.items() if v is not None)


def run(name: str, text: str, should_work: bool) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "config.txt"
        path.write_text(text, encoding="utf-8")
        try:
            result = load_config(str(path))
        except ConfigError as e:
            status = "FAIL" if should_work else "PASS"
            print(f"{status}  {name}  ->  ERROR: {e}")
        else:
            status = "PASS" if should_work else "FAIL"
            print(f"{status}  {name}  ->  {result}")


if __name__ == "__main__":
    # should work
    run("good config", make_text(), True)
    run("comments and spaces",
        "# hello\n\nWIDTH = 20\nHEIGHT=15\nENTRY=0, 0\n"
        "EXIT=19,14\nOUTPUT_FILE=maze.txt\nPERFECT=False\n", True)

    # should raise a ConfigError
    run("missing key", make_text(HEIGHT=None), False)
    run("WIDTH not a number", make_text(WIDTH="abc"), False)
    run("WIDTH is zero", make_text(WIDTH="0"), False)
    run("WIDTH negative", make_text(WIDTH="-5"), False)
    run("ENTRY one number", make_text(ENTRY="5"), False)
    run("ENTRY three numbers", make_text(ENTRY="1,2,3"), False)
    run("ENTRY not numbers", make_text(ENTRY="a,b"), False)
    run("ENTRY x out of bounds", make_text(ENTRY="20,0"), False)
    run("EXIT y out of bounds", make_text(EXIT="0,15"), False)
    run("ENTRY equals EXIT", make_text(ENTRY="3,3", EXIT="3,3"), False)
    run("PERFECT invalid", make_text(PERFECT="maybe"), False)
    run("no equal sign", "WIDTH 20\n", False)
    run("duplicate key", make_text() + "\nWIDTH=30\n", False)
    run("empty file", "", False)

    # file errors
    try:
        load_config("nope.txt")
    except ConfigError as e:
        print(f"PASS  missing file  ->  ERROR: {e}")