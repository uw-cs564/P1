SELECT ID, MAX(currently) as highestCurr 
FROM Item 
WHERE currently = highestCurr;