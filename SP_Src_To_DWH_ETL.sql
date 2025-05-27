CREATE PROCEDURE dbo.usp_LoadDataWarehouse_SCD2_Full
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @Today DATE = CAST(GETDATE() AS DATE);

    -- 1. Load DimDate (from order and transaction dates)
    INSERT INTO DimDate (DateKey, Date, Year, Quarter, Month, Day, Week, DayOfWeek)
    SELECT DISTINCT
        CONVERT(INT, FORMAT(OrderDate, 'yyyyMMdd')) AS DateKey,
        OrderDate,
        YEAR(OrderDate),
        DATEPART(QUARTER, OrderDate),
        MONTH(OrderDate),
        DAY(OrderDate),
        DATEPART(WEEK, OrderDate),
        DATEPART(WEEKDAY, OrderDate)
    FROM online_order_aligned
    WHERE NOT EXISTS (
        SELECT 1 FROM DimDate WHERE DateKey = CONVERT(INT, FORMAT(OrderDate, 'yyyyMMdd'))
    )
    UNION
    SELECT DISTINCT
        CONVERT(INT, FORMAT(TransactionDate, 'yyyyMMdd')) AS DateKey,
        TransactionDate,
        YEAR(TransactionDate),
        DATEPART(QUARTER, TransactionDate),
        MONTH(TransactionDate),
        DAY(TransactionDate),
        DATEPART(WEEK, TransactionDate),
        DATEPART(WEEKDAY, TransactionDate)
    FROM loyalty_points_transaction
    WHERE NOT EXISTS (
        SELECT 1 FROM DimDate WHERE DateKey = CONVERT(INT, FORMAT(TransactionDate, 'yyyyMMdd'))
    );

    -- 2. SCD2 for DimCustomer
    UPDATE d
    SET EndDate = @Today, IsCurrent = 0
    FROM DimCustomer d
    JOIN customer s ON d.CustomerID = s.CustomerID
    WHERE d.IsCurrent = 1
      AND (
            ISNULL(d.FirstName, '') <> ISNULL(s.FirstName, '')
         OR ISNULL(d.LastName, '') <> ISNULL(s.LastName, '')
         OR ISNULL(d.Email, '') <> ISNULL(s.Email, '')
      );

    INSERT INTO DimCustomer (CustomerID, FirstName, LastName, Email, StartDate, EndDate, IsCurrent)
    SELECT
        s.CustomerID, s.FirstName, s.LastName, s.Email, @Today, NULL, 1
    FROM customer s
    LEFT JOIN DimCustomer d
      ON s.CustomerID = d.CustomerID AND d.IsCurrent = 1
    WHERE d.CustomerID IS NULL
       OR (
            ISNULL(d.FirstName, '') <> ISNULL(s.FirstName, '')
         OR ISNULL(d.LastName, '') <> ISNULL(s.LastName, '')
         OR ISNULL(d.Email, '') <> ISNULL(s.Email, '')
       );

    -- 3. SCD2 for DimProduct
    UPDATE d
    SET EndDate = @Today, IsCurrent = 0
    FROM DimProduct d
    JOIN product s ON d.ProductID = s.ProductID
    WHERE d.IsCurrent = 1
      AND (
            ISNULL(d.ProductName, '') <> ISNULL(s.ProductName, '')
         OR ISNULL(d.CategoryID, '') <> ISNULL(s.CategoryID, '')
         OR ISNULL(d.UnitPrice, 0) <> ISNULL(s.UnitPrice, 0)
      );

    INSERT INTO DimProduct (ProductID, ProductName, CategoryID, UnitPrice, StartDate, EndDate, IsCurrent)
    SELECT
        s.ProductID, s.ProductName, s.CategoryID, s.UnitPrice, @Today, NULL, 1
    FROM product s
    LEFT JOIN DimProduct d
      ON s.ProductID = d.ProductID AND d.IsCurrent = 1
    WHERE d.ProductID IS NULL
       OR (
            ISNULL(d.ProductName, '') <> ISNULL(s.ProductName, '')
         OR ISNULL(d.CategoryID, '') <> ISNULL(s.CategoryID, '')
         OR ISNULL(d.UnitPrice, 0) <> ISNULL(s.UnitPrice, 0)
       );

    -- 4. SCD2 for DimStore
    UPDATE d
    SET EndDate = @Today, IsCurrent = 0
    FROM DimStore d
    JOIN store s ON d.StoreID = s.StoreID
    WHERE d.IsCurrent = 1
      AND (
            ISNULL(d.StoreName, '') <> ISNULL(s.StoreName, '')
         OR ISNULL(d.City, '') <> ISNULL(s.City, '')
         OR ISNULL(d.State, '') <> ISNULL(s.State, '')
         OR ISNULL(d.Country, '') <> ISNULL(s.Country, '')
      );

    INSERT INTO DimStore (StoreID, StoreName, City, State, Country, StartDate, EndDate, IsCurrent)
    SELECT
        s.StoreID, s.StoreName, s.City, s.State, s.Country, @Today, NULL, 1
    FROM store s
    LEFT JOIN DimStore d
      ON s.StoreID = d.StoreID AND d.IsCurrent = 1
    WHERE d.StoreID IS NULL
       OR (
            ISNULL(d.StoreName, '') <> ISNULL(s.StoreName, '')
         OR ISNULL(d.City, '') <> ISNULL(s.City, '')
         OR ISNULL(d.State, '') <> ISNULL(s.State, '')
         OR ISNULL(d.Country, '') <> ISNULL(s.Country, '')
       );

    -- 5. SCD2 for DimLoyaltyProgram
    UPDATE d
    SET EndDate = @Today, IsCurrent = 0
    FROM DimLoyaltyProgram d
    JOIN loyalty_program s ON d.LoyaltyProgramID = s.LoyaltyProgramID
    WHERE d.IsCurrent = 1
      AND (
            ISNULL(d.ProgramName, '') <> ISNULL(s.ProgramName, '')
         OR ISNULL(d.StartDate, '') <> ISNULL(s.StartDate, '')
         OR ISNULL(d.EndDate, '') <> ISNULL(s.EndDate, '')
      );

    INSERT INTO DimLoyaltyProgram (LoyaltyProgramID, ProgramName, StartDate, EndDate, StartDateDW, EndDateDW, IsCurrent)
    SELECT
        s.LoyaltyProgramID, s.ProgramName, s.StartDate, s.EndDate, @Today, NULL, 1
    FROM loyalty_program s
    LEFT JOIN DimLoyaltyProgram d
      ON s.LoyaltyProgramID = d.LoyaltyProgramID AND d.IsCurrent = 1
    WHERE d.LoyaltyProgramID IS NULL
       OR (
            ISNULL(d.ProgramName, '') <> ISNULL(s.ProgramName, '')
         OR ISNULL(d.StartDate, '') <> ISNULL(s.StartDate, '')
         OR ISNULL(d.EndDate, '') <> ISNULL(s.EndDate, '')
       );

    -- 6. SCD2 for DimShipmentCarrier
    UPDATE d
    SET EndDate = @Today, IsCurrent = 0
    FROM DimShipmentCarrier d
    JOIN carrier s ON d.CarrierID = s.CarrierID
    WHERE d.IsCurrent = 1
      AND ISNULL(d.CarrierName, '') <> ISNULL(s.CarrierName, '');

    INSERT INTO DimShipmentCarrier (CarrierID, CarrierName, StartDate, EndDate, IsCurrent)
    SELECT
        s.CarrierID, s.CarrierName, @Today, NULL, 1
    FROM carrier s
    LEFT JOIN DimShipmentCarrier d
      ON s.CarrierID = d.CarrierID AND d.IsCurrent = 1
    WHERE d.CarrierID IS NULL
       OR ISNULL(d.CarrierName, '') <> ISNULL(s.CarrierName, '');

    -- 7. Standard load for other dimensions (no SCD)
    INSERT INTO DimCampaign (CampaignID, ChannelID, StartDate, EndDate, Budget)
    SELECT DISTINCT
        c.CampaignID, c.ChannelID, c.StartDate, c.EndDate, c.Budget
    FROM marketing_campaign c
    LEFT JOIN DimCampaign d ON c.CampaignID = d.CampaignID
    WHERE d.CampaignID IS NULL;

    INSERT INTO DimProductCategory (CategoryID, CategoryName)
    SELECT DISTINCT
        c.CategoryID, c.CategoryName
    FROM product_category c
    LEFT JOIN DimProductCategory d ON c.CategoryID = d.CategoryID
    WHERE d.CategoryID IS NULL;

    -- 8. Fact table loads (always join to IsCurrent=1 for SCD2 dims)
    INSERT INTO FactOnlineOrder (OnlineOrderID, CustomerKey, StoreKey, OrderDateKey, TotalAmount)
    SELECT
        o.OnlineOrderID,
        dc.CustomerKey,
        ds.StoreKey,
        CONVERT(INT, FORMAT(o.OrderDate, 'yyyyMMdd')) AS OrderDateKey,
        o.TotalAmount
    FROM online_order_aligned o
    JOIN DimCustomer dc ON o.CustomerID = dc.CustomerID AND dc.IsCurrent = 1
    JOIN DimStore ds ON o.StoreID = ds.StoreID AND ds.IsCurrent = 1
    LEFT JOIN FactOnlineOrder fo ON o.OnlineOrderID = fo.OnlineOrderID
    WHERE fo.OnlineOrderID IS NULL;

    INSERT INTO FactOnlineOrderLine (OrderLineID, OnlineOrderKey, ProductKey, Quantity, UnitPrice)
    SELECT
        l.OrderLineID,
        fo.OnlineOrderKey,
        dp.ProductKey,
        l.Quantity,
        l.UnitPrice
    FROM online_order_line l
    JOIN FactOnlineOrder fo ON l.OrderID = fo.OnlineOrderID
    JOIN DimProduct dp ON l.ProductID = dp.ProductID AND dp.IsCurrent = 1
    LEFT JOIN FactOnlineOrderLine fl ON l.OrderLineID = fl.OrderLineID
    WHERE fl.OrderLineID IS NULL;

    INSERT INTO FactLoyaltyPointsTransaction (PointsTransactionID, CustomerKey, LoyaltyProgramKey, TransactionDateKey, Points)
    SELECT
        l.PointsTransactionID,
        dc.CustomerKey,
        dlp.LoyaltyProgramKey,
        CONVERT(INT, FORMAT(l.TransactionDate, 'yyyyMMdd')) AS TransactionDateKey,
        l.Points
    FROM loyalty_points_transaction l
    JOIN DimCustomer dc ON l.CustomerID = dc.CustomerID AND dc.IsCurrent = 1
    JOIN DimLoyaltyProgram dlp ON l.LoyaltyProgramID = dlp.LoyaltyProgramID AND dlp.IsCurrent = 1
    LEFT JOIN FactLoyaltyPointsTransaction fl ON l.PointsTransactionID = fl.PointsTransactionID
    WHERE fl.PointsTransactionID IS NULL;

    INSERT INTO FactCampaignResponse (CampaignID, CustomerKey, ResponseDateKey)
    SELECT
        r.CampaignID,
        dc.CustomerKey,
        CONVERT(INT, FORMAT(r.ResponseDate, 'yyyyMMdd')) AS ResponseDateKey
    FROM campaign_response r
    JOIN DimCustomer dc ON r.CustomerID = dc.CustomerID AND dc.IsCurrent = 1
    LEFT JOIN FactCampaignResponse fcr
        ON r.CampaignID = fcr.CampaignID AND dc.CustomerKey = fcr.CustomerKey AND CONVERT(INT, FORMAT(r.ResponseDate, 'yyyyMMdd')) = fcr.ResponseDateKey
    WHERE fcr.CampaignID IS NULL;

    -- Add more fact/dimension loads as needed

END
GO