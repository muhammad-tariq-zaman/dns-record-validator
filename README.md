# dns-record-validator

Validate simple DNS zone-file lines for A, AAAA, MX, CNAME and TXT records and report the bad lines.

## How to run

```sh
python3 main.py zone.txt
```

## Example output

```
line 2: bad IPv4 address: 999.1.1.1
1 invalid record(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
