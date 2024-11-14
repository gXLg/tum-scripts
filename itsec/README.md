# IT Security

## Login
Obtain/refresh your login cookie by executing `login.py`.

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
The parsed URL, password and the
`flag` function, which accepts a string,
searches for a flag using regex and prints it out,
will be put into the file `header.txt`
inside the task folder.

## Submit
Submit a flag using `submit <flag>`.

## Upload
Upload your code using `upload <number>`.
This will upload the file `pwn_students.py`
from your task folder.
