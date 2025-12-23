import argparse
import os
import stat
from pathlib import Path

# aoc get-input [year] [day]
# aoc run [year] [day]
# aoc submit [year] [day]
from http.cookiejar import MozillaCookieJar
from urllib import request

def _setup_session(cookie_filename="cookies.txt"):
    cj = MozillaCookieJar("./cookies.txt")
    cj.load()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    request.install_opener(opener)


def _download_input(year, day, ):
    resp = request.urlopen(f"https://adventofcode.com/{year}/day/{day}/input")
    return resp.read().decode()


def _get():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)

    args = parser.parse_args()

    inp_filename = Path.cwd() / "inputs" / f"{args.year}" / f"{args.day:02d}.txt"
    if inp_filename.exists():
        with open(inp_filename) as fobj:
            print(fobj.read())
        return 0

    _setup_session()
    inp = _download_input(args.year, args.day)
    inp_filename.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    with open(inp_filename, mode="w") as fobj:
        fobj.write(inp)
    os.chmod(inp_filename, stat.S_IREAD)
    print(inp)


if __name__ == "__main__":
    _get()
