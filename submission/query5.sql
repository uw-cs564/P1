    SELECT COUNT(*) FROM (SELECT DISTINCT Users.UserID, Users.Rating
    FROM Users,Item 
    WHERE Users.UserID = Item.SellerID) WHERE Rating > 1000;