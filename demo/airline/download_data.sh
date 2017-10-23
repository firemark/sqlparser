#!/usr/bin/env sh
set -e
rm *.csv -f
rm data.zip -f
wget 'https://www.transtats.bts.gov/DownLoad_Table.asp?Table_ID=236&Has_Group=3&Is_Zipped=0' --post-file=data_post -O data.zip
unzip data.zip
mv *.csv data.csv
sed -i s/,$// data.csv
