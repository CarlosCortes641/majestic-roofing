#!/usr/bin/env python3
import re
import urllib.error
import urllib.parse
import urllib.request
import http.cookiejar

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
html = opener.open("http://localhost:5130/").read().decode()
m = re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', html)
if not m:
    m = re.search(r'value="([^"]+)"[^>]*name="__RequestVerificationToken"', html)
print("has token", bool(m))
print("form action present", "/leads/contact" in html)
i = html.find("contact-form")
print(html[i : i + 450])
if not m:
    raise SystemExit(1)

data = urllib.parse.urlencode(
    {
        "__RequestVerificationToken": m.group(1),
        "Name": "Test User",
        "Phone": "9808005991",
        "Email": "test@example.com",
        "Address": "123 Main St Charlotte NC",
        "Service": "inspection",
        "Issue": "hail-storm",
        "Details": "Demo lead",
        "Language": "English",
    }
).encode()
req = urllib.request.Request("http://localhost:5130/leads/contact", data=data, method="POST")
req.add_header("Content-Type", "application/x-www-form-urlencoded")
req.add_header("Referer", "http://localhost:5130/")
try:
    resp = opener.open(req)
    print("status", resp.status, resp.geturl())
except urllib.error.HTTPError as e:
    print("error", e.code, e.read()[:400])
    raise

ops = opener.open("http://localhost:5130/ops").read().decode()
print("ops has Test User", "Test User" in ops)
print("ops has MJ", "MJ-" in ops)
