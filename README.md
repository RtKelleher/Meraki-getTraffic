# Meraki-getTraffic
Simple Python3 script to pull 3 relevant data streams via Meraki-API to /var/log for Splunk ingestion via crontab

e.g. `crontab -e */5 * * * * /usr/bin/python3 ./getTraffic.py >/dev/null 2>&1` 
