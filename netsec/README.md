# Network Security

Similar to [IT Security](../itsec), only with different endpoints
and a better arguments system.

## Login
Obtain/refresh your login cookie by executing `login`.

Put your shib credentials in a file called `shib.txt`
in following format:
```
<username/email> <new line>
<password>
```
Login cookies will be saved in a file called `cookie`

## Download
Download the task using `download <number>`.

This will download and unzip the task
into the folder `task_<padded number>`.
The parsed URL, optionally host, port and password and the
`flag` function, which accepts a string,
searches for a flag using regex and prints it out,
will be put into the file `header.txt`
inside the task folder.

## Submit
Submit a flag using `submit <flag>`.
It will output the feedback provided on the page, which
can be one of three things:
* Wrong flag
* An already used flag
* Correct flag (+ name of the task)

Or submit a file automatically using `submit <python file>`.
It will run the script, capture the flag and submit it.

## Upload
Upload your code using `upload [file]`.
This will upload the file `pwn_students.py` or `pwn-students.py`,
or `file` if provided.

## Polling
If you are participating in the challenge and want to compete
for the fastest flag capture, but the current course moderators
are unpunctual, delay the release or the release time is not known,
you can use the following line with an alert of your choice to notify
you when the task is released:
```
while ! download <task_number>; do sleep 5; done;
# a visible or audible alert like:
mpv --no-video ~/Downloads/alert.mp3
```

## Team ID
During the exercises, it occurred that you may need your Team ID.
If you have changed your team name, then it is not possible to find
your ID visually anywhere.

For this case, you may use the following python script
to find out your original Team ID:
```py
from requests import Session
from bs4 import BeautifulSoup as BS

# provided in the parent folder
from shibboleth import login

username = "" # TODO
password = "" # TODO

cookies = login("netsec", username, password)

BASE = "https://netsec.net.in.tum.de"
with Session() as s:
  s.cookies = cookies

  r = s.get(BASE + "/team")
  b = BS(r.text, "html.parser")
  current = b.find("input", { "name": "teamname" })["value"]
  print("Current team name:", current)

  number = 1
  while True:
    r = s.post(BASE + "/team/changename", data={"teamname": f"Team {number}"})
    b = BS(r.text, "html.parser")
    if b.find("div", { "class": "alert-message" }) is None:
      print("Team ID found:", number)
      print("Restoring team name...")
      s.post(BASE + "/team/changename", data={"teamname": current})
      break
    number += 1
```

The module `shibboleth` is provided in the parent folder.
You can either:
```
ln -s <shib path> ./shibboleth
python script.py
```
or
```
PYTHONPATH="<full path to tum-scripts>:$PYTHONPATH" python script.py
```
