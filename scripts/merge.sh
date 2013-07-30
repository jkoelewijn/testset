export LC_ALL=C

rm alltests.zip
java -jar bin/onebusaway-gtfs-transformer-cli.jar --overwriteDuplicates `ls -1 results/*zip | head -n 1` `ls -1 results/*zip | tail -n +2 | head -n 1` alltests.zip

ls -1 results/*zip | tail -n +3 | while read i; do
	java -jar bin/onebusaway-gtfs-transformer-cli.jar --overwriteDuplicates alltests.zip "$i" alltests.zip
done
