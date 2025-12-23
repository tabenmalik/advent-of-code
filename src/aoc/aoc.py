
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

def get_input():
    ...
