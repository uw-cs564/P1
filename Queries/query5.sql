Sellers AS (SELECT * FROM USERS WHERE LOCATION IS NULL AND COUNTRY_CODE IS NULL), SELECT * FROM Sellers WHERE Rating > 1000;