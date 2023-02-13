#!/bin/bash

# --days Query the previous N days with this rule
# --start YYYY-MM-DDTHH:MM:SS Start querying from this timestamp
# --end YYYY-MM-DDTHH:MM:SS Query to this timestamp

for f in /opt/so/rules/elastalert/playbook/*.yaml
do
	f1=`basename $f`
	echo "Processing playbook/$f1"
	docker exec -it so-elastalert elastalert-test-rule /opt/elastalert/rules/playbook/$f1 --config /opt/elastalert/config.yaml --alert --start $1 --end $2 
done
