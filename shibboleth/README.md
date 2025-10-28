# TUM Shibboleth

A general shibboleth login tool.

CLI:
```
Usage: python -m shibboleth [OPTIONS] [SERVICE]

Options:
  -f, --file FILENAME  File to extract username and password, use '-' or omit
                       the option to read from stdin
  -q, --quiet          Disable info output
  --list               List pre-defined services
  --help               Show this message and exit.
```
`Service` is either a pre-defined service name like `netsec` or `tum.live`,
or a shibboleth login link like `https://scoreboard.sec.in.tum.de/shib-login`

Module:
```
from shibboleth import login

login(service, username, password) -> CookieJar
```
