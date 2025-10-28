from .core import login, services
from sys import argv
from click import command, argument, option, File, UsageError

@command()
@option("-f", "--file", default="-", help="File to extract username and password, use '-' or omit the option to read from stdin", type=File("r"))
@option("-q", "--quiet", is_flag=True, help="Disable info output")
@option("--list", is_flag=True, help="List pre-defined services")
@argument("service", required=False)
def main(file, quiet, list, service):
  if list:
    for s in services:
      print(f"{s}: {services[s]}")
    return

  if service is None:
    raise UsageError("Missing argument 'SERVICE'.")

  try:
    username, password, *_ = file.read().strip().split("\n")
  except Exception:
    exit("Error parsing user credentials")

  cookies = login(service, username, password, not quiet)

  # print cookies
  c = []
  for i in cookies:
    c.append(i.name + "=" + i.value)
  print("; ".join(c))

if __name__ == "__main__":
  main()
