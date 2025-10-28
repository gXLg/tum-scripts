import requests
from bs4 import BeautifulSoup as BS
from sys import stderr

services = {
  "tum.live": "https://tum.live/saml/out",
  "netsec": "https://netsec.net.in.tum.de/login",
  "itsec": "https://scoreboard.sec.in.tum.de/shib-login"
}

def login(shib, username, password, info=False):
  def print_info(*args):
    if info: print(*args, file=stderr)

  print_info("Logging in as", username)

  if shib in services:
    shib = services[shib]

  with requests.Session() as s:
    # landing page
    r = s.get(shib, headers={"User-Agent": "Mozilla/5.0"})
    print_info("Shibboleth SSO   |", r.status_code)
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
    print_info("Login Page       |", r.status_code)
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
    print_info("Login Processing |", r.status_code)
    b = BS(r.text, "html.parser")
    if b.find("input", { "name": "RelayState" }) is None:
      raise Exception("Wrong credentials supplied")

    url = b.find("form")["action"]
    data = {
      "RelayState": b.find("input", { "name": "RelayState" })["value"],
      "SAMLResponse": b.find("input", { "name": "SAMLResponse" })["value"]
    }

    # redirect back to platform
    r = s.post(url, data=data)
    print_info("Final:", r.status_code, "|", r.url)

    return s.cookies

def login_txt(shib, file, info=False):
  try:
    username, password, *_ = file.read().strip().split("\n")
  except Exception:
    raise Exception("Error parsing user credentials")

  return login(shib, username, password, info)
