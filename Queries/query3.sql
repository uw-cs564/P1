fourCat AS (SELECT itemID, COUNT(*) as numCat FROM Category WHERE numCat = 4), SELECT COUNT(*) FROM fourCat;