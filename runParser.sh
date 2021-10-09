rm ./data/*.dat

END=39
for ((i=0;i<=END;i++)); do
	python parser.py ebay_data/items-$i.json
    echo $i
done

sort -u data/bids.dat -o data/bids.dat
sort -u data/category.dat -o data/category.dat
sort -u data/items.dat -o data/items.dat
sort -u data/users.dat -o data/users.dat
