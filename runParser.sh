rm ./data/*.dat

END=39
for ((i=0;i<=END;i++)); do
	python parser.py ebay_data/items-$i.json
    echo $i
done