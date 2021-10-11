WITH fourCat AS (
SELECT ItemID, COUNT(Category_Name) AS numCat 
FROM Category 
GROUP BY ItemID
HAVING numCat = 4)
SELECT COUNT(*) FROM fourCat;