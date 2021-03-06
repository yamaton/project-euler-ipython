"""
Quick and dirty script to get project euler problem descriptions

Required libraries
==================
- [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/)

Usage:
======
```
$ python scrape_project_euler.py <problem-id>
```
<problem-id> should be a number, like 42.
The script produces Markdown/HTML styled text as standard output.

@author yamaton
@date 2015-10-14
"""

import sys
import urllib.request
import bs4

BASE = "https://projecteuler.net/problem={}"


def get_raw(problem_id):
    url = BASE.format(problem_id)
    with urllib.request.urlopen(url) as f:
        rawhtml = f.read()
    return rawhtml


def _scrape_euler_page(raw):
    """
    Scrape html and return dictionary with keys
        'id'      (int)
        'title'   (str)
        'url'     (str)
        'content' (soup)
    """
    soup = bs4.BeautifulSoup(raw, "html.parser")
    tmp = soup.find("h3").get_text()
    prob_id = int(tmp.replace("Problem ", "").split()[0])
    url = BASE.format(prob_id)
    title = soup.find("h2").get_text()
    content = soup.find("div", "problem_content")

    return {"id": prob_id, "url": url, "title": title, "content": content}


def _add_quote(element_tag):
    lines = ["> " + str(line).replace("\n", "") for line in element_tag if str(line).strip()]
    return "\n".join(lines)


def _format_data(data):
    lines = [
        f"## Problem {data['id']}",
        "",
        f"[{data['title']}]({data['url']})",
        "",
        _add_quote(data["content"]),
    ]
    return "\n".join(lines)


def get_formatted(problem_num):
    raw = get_raw(problem_num)
    data = _scrape_euler_page(raw)
    return _format_data(data)


def main():
    if len(sys.argv) < 2:
        sys.exit(f"Usage: python {sys.argv[0]} <problem-number>")

    problem_num = int(sys.argv[1])
    s = get_formatted(problem_num)
    print(s)


if __name__ == "__main__":
    main()
