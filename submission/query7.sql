ItemPrices AS
    (SELECT Item_ID 
    FROM Bid
    WHERE Amount > 100
    GROUP BY Item_ID),
SELECT Category_Name 
FROM CATEGORY c,ItemPrices ip
WHERE c.Item_ID = ip.Item_ID
GROUP BY Category_Name
