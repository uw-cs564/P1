rm ./*.dat

END=39
for ((i=0;i<=END;i++)); do
	python parser.py ebay_data/items-$i.json
    echo $i
done

sort -u bids.dat -o bids.dat
sort -u category.dat -o category.dat
sort -u items.dat -o items.dat
sort -u users.dat -o users.dat
