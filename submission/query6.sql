SELECT COUNT(distinct Seller_ID) 
FROM Item 
WHERE Seller_ID IN (SELECT SELECT Bidder_ID FROM Bid)