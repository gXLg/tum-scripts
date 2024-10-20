# IT Security

# Login
Obtain/refresh your login cookie by executing `login.py`.

Put your shib credentials in a file called `shib.txt`
in following format:
```
<username/email> <new line>
<password>
```
Login cookies will be saved in a file called `cookie`

# Download
Download the task using `download <number>`.

This will download and unzip the task
into the folder `task_<padded number>`
and create a dummy file called `exploit.py`
with some imports, the flag `URL` and the
`flag` function, which accepts a string,
searches for a flag using regex and prints it out.

# Submit
Submit a flag using `submit <flag>`.
