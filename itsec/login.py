# Login into scoreboard using shibboleth

import requests
from bs4 import BeautifulSoup as BS

with open("shib.txt", "r") as f:
  username, password = f.read().strip().split("\n")

with requests.Session() as s:
  # landing page
  r = s.get("https://scoreboard.sec.in.tum.de/shib-login")
  b = BS(r.text, "html.parser")
  url = "https://login.tum.de" + b.find("form", { "name": "form1" })["action"]
  data = {
    "csrf_token": b.find("input", { "name": "csrf_token" })["value"],
    "shib_idp_ls_exception.shib_idp_session_ss": "",
    "shib_idp_ls_success.shib_idp_session_ss": "true",
    "shib_idp_ls_value.shib_idp_session_ss": "",
    "shib_idp_ls_exception.shib_idp_persistent_ss": "",
    "shib_idp_ls_success.shib_idp_persistent_ss": "true",
    "shib_idp_ls_value.shib_idp_persistent_ss": "",
    "shib_idp_ls_supported": "true",
    "_eventId_proceed": ""
  }

  # login page
  r = s.post(url, data=data)
  b = BS(r.text, "html.parser")
  url = "https://login.tum.de" + b.find("form")["action"]
  data = {
    "csrf_token": b.find("input", { "name": "csrf_token" })["value"],
    "j_username": username,
    "j_password": password,
    "donotcache-dummy": 1,
    "donotcache": "",
    "_eventId_proceed": ""
  }

  # login processing
  r = s.post(url, data=data)
  b = BS(r.text, "html.parser")
  url = b.find("form")["action"]
  data = {
    "RelayState": b.find("input", { "name": "RelayState" })["value"],
    "SAMLResponse": b.find("input", { "name": "SAMLResponse" })["value"]
  }

  # redirect back to platform
  r = s.post(url, data=data)
  if r.url == "https://scoreboard.sec.in.tum.de/scoreboard":
    print("Login successful!")
  else:
    exit("Login failed!")

  # save cookies
  c = []
  for i in s.cookies:
    c.append(i.name + "=" + i.value)

  with open("cookie", "w") as f:
    f.write("; ".join(c))
