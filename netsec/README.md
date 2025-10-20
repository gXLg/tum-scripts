# Network Security

Similar to [IT Security](../itsec), only with different endpoints
and a better arguments system.

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
