Sellers AS 
    (SELECT Rating 
    FROM Users,Item 
    WHERE Users.ID = Item.Seller_ID GROUP BY Item.Seller_ID), 
SELECT COUNT(*) FROM Sellers WHERE Rating > 1000;