# Salesforce download logs
## Usage

```
$ python logs.py --help
usage: logs.py [-h] [--date date]
               login_url client_id client_secret username password

Download and parse Salesforce Log file.

positional arguments:
  login_url      Login url to Salesforce (production or sandbox)
  client_id      Salesforce application client_id used to login
  client_secret  Salesforce application client_secret used to login
  username       User name for login
  password       User password for login

optional arguments:
  -h, --help     show this help message and exit
  --date date    Optional date from which take logs. If not pass it is set to
                 YESTERDAY
```


## Required libraries

- argparse
- requests
- pprint


