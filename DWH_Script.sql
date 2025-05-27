CREATE TABLE DimCustomer (
    CustomerKey INT IDENTITY(1,1) PRIMARY KEY,         -- Surrogate Key
    CustomerID VARCHAR(50) NOT NULL UNIQUE,            -- Business Key
    FirstName NVARCHAR(100),
    LastName NVARCHAR(100),
    Email NVARCHAR(255),
	BirthDate nvarchar(255) NULL,
	[SignupDate] [nvarchar](255) NULL,
	[Gender] [nvarchar](255) NULL,
	[City] [nvarchar](255) NULL,
	[State] [nvarchar](255) NULL,
	[Country] [nvarchar](255) NULL
    -- Add other customer attributes as needed
    -- e.g., Gender, DateOfBirth, etc.
);


CREATE TABLE DimProduct (
    ProductKey INT IDENTITY(1,1) PRIMARY KEY,          -- Surrogate Key
    ProductID VARCHAR(50) NOT NULL UNIQUE,             -- Business Key
    ProductName NVARCHAR(255),
    CategoryID VARCHAR(50),
    UnitPrice DECIMAL(18,2),
    -- Add other product attributes as needed
);


CREATE TABLE DimStore (
    StoreKey INT IDENTITY(1,1) PRIMARY KEY,
    StoreID VARCHAR(50) NOT NULL UNIQUE,
    StoreName NVARCHAR(255),
    City NVARCHAR(100),
    State NVARCHAR(100),
    Country NVARCHAR(100)
    -- Add other store attributes as needed
);


CREATE TABLE DimDate (
    DateKey INT PRIMARY KEY,           -- Format: YYYYMMDD
    Date DATE NOT NULL,
    Year INT,
    Quarter INT,
    Month INT,
    Day INT,
    Week INT,
    DayOfWeek INT
);


CREATE TABLE DimLoyaltyProgram (
    LoyaltyProgramKey INT IDENTITY(1,1) PRIMARY KEY,
    LoyaltyProgramID VARCHAR(50) NOT NULL UNIQUE,
    ProgramName NVARCHAR(255),
    StartDate DATE,
    EndDate DATE
);



CREATE TABLE DimCampaign (
    CampaignKey INT IDENTITY(1,1) PRIMARY KEY,
    CampaignID VARCHAR(50) NOT NULL UNIQUE,
    ChannelID VARCHAR(50),
    StartDate DATE,
    EndDate DATE,
    Budget DECIMAL(18,2)
);



CREATE TABLE DimProductCategory (
    CategoryKey INT IDENTITY(1,1) PRIMARY KEY,
    CategoryID VARCHAR(50) NOT NULL UNIQUE,
    CategoryName NVARCHAR(255)
);




CREATE TABLE FactOnlineOrder (
    OnlineOrderKey INT IDENTITY(1,1) PRIMARY KEY,
    OnlineOrderID VARCHAR(50) NOT NULL UNIQUE,         -- Business Key
    CustomerKey INT NOT NULL,
    StoreKey INT NOT NULL,
    OrderDateKey INT NOT NULL,
    TotalAmount DECIMAL(18,2),
    -- Foreign Keys
    FOREIGN KEY (CustomerKey) REFERENCES DimCustomer(CustomerKey),
    FOREIGN KEY (StoreKey) REFERENCES DimStore(StoreKey),
    FOREIGN KEY (OrderDateKey) REFERENCES DimDate(DateKey)
);


CREATE TABLE FactOnlineOrderLine (
    OrderLineKey INT IDENTITY(1,1) PRIMARY KEY,
    OrderLineID VARCHAR(50) NOT NULL UNIQUE,
    OnlineOrderKey INT NOT NULL,
    ProductKey INT NOT NULL,
    Quantity INT,
    UnitPrice DECIMAL(18,2),
    -- Foreign Keys
    FOREIGN KEY (OnlineOrderKey) REFERENCES FactOnlineOrder(OnlineOrderKey),
    FOREIGN KEY (ProductKey) REFERENCES DimProduct(ProductKey)
);


CREATE TABLE FactLoyaltyPointsTransaction (
    PointsTransactionKey INT IDENTITY(1,1) PRIMARY KEY,
    PointsTransactionID VARCHAR(50) NOT NULL UNIQUE,
    CustomerKey INT NOT NULL,
    LoyaltyProgramKey INT NOT NULL,
    TransactionDateKey INT NOT NULL,
    Points INT,
    -- Foreign Keys
    FOREIGN KEY (CustomerKey) REFERENCES DimCustomer(CustomerKey),
    FOREIGN KEY (LoyaltyProgramKey) REFERENCES DimLoyaltyProgram(LoyaltyProgramKey),
    FOREIGN KEY (TransactionDateKey) REFERENCES DimDate(DateKey)
);



CREATE TABLE FactCampaignResponse (
    CampaignResponseKey INT IDENTITY(1,1) PRIMARY KEY,
    CampaignID VARCHAR(50) NOT NULL,
    CustomerKey INT NOT NULL,
    ResponseDateKey INT NOT NULL,
    -- Foreign Keys
    FOREIGN KEY (CampaignID) REFERENCES DimCampaign(CampaignID),
    FOREIGN KEY (CustomerKey) REFERENCES DimCustomer(CustomerKey),
    FOREIGN KEY (ResponseDateKey) REFERENCES DimDate(DateKey)
);



CREATE TABLE DimStoreEvent (
    StoreEventKey INT IDENTITY(1,1) PRIMARY KEY,
    StoreEventID VARCHAR(50) NOT NULL UNIQUE,   -- Business Key
    StoreKey INT NOT NULL,
    EventName NVARCHAR(255),
    EventDate DATE,
    -- Foreign Key
    FOREIGN KEY (StoreKey) REFERENCES DimStore(StoreKey)
);

CREATE TABLE DimPromotion (
    PromotionKey INT IDENTITY(1,1) PRIMARY KEY,
    PromotionID VARCHAR(50) NOT NULL UNIQUE,    -- Business Key
    PromotionName NVARCHAR(255),
    StartDate DATE,
    EndDate DATE,
    DiscountPercentage INT,
    -- Add other attributes as needed
);



CREATE TABLE DimShipmentCarrier (
    CarrierKey INT IDENTITY(1,1) PRIMARY KEY,
    CarrierID VARCHAR(50) NOT NULL UNIQUE,      -- Business Key
    CarrierName NVARCHAR(255)
);


CREATE TABLE FactStoreEventAttendance (
    StoreEventAttendanceKey INT IDENTITY(1,1) PRIMARY KEY,
    StoreEventKey INT NOT NULL,
    CustomerKey INT NOT NULL,
    AttendanceDateKey INT NOT NULL,
    -- Foreign Keys
    FOREIGN KEY (StoreEventKey) REFERENCES DimStoreEvent(StoreEventKey),
    FOREIGN KEY (CustomerKey) REFERENCES DimCustomer(CustomerKey),
    FOREIGN KEY (AttendanceDateKey) REFERENCES DimDate(DateKey)
);




CREATE TABLE FactPromotionRedemption (
    PromotionRedemptionKey INT IDENTITY(1,1) PRIMARY KEY,
    PromotionKey INT NOT NULL,
    CustomerKey INT NOT NULL,
    ProductKey INT NOT NULL,
    RedemptionDateKey INT NOT NULL,
    RedemptionAmount DECIMAL(18,2),
    -- Foreign Keys
    FOREIGN KEY (PromotionKey) REFERENCES DimPromotion(PromotionKey),
    FOREIGN KEY (CustomerKey) REFERENCES DimCustomer(CustomerKey),
    FOREIGN KEY (ProductKey) REFERENCES DimProduct(ProductKey),
    FOREIGN KEY (RedemptionDateKey) REFERENCES DimDate(DateKey)
);




CREATE TABLE FactShipment (
    ShipmentKey INT IDENTITY(1,1) PRIMARY KEY,
    ShipmentID VARCHAR(50) NOT NULL UNIQUE,     -- Business Key
    OrderKey INT NOT NULL,
    CarrierKey INT NOT NULL,
    ShipmentDateKey INT NOT NULL,
    Status NVARCHAR(50),
    -- Foreign Keys
    FOREIGN KEY (OrderKey) REFERENCES FactOnlineOrder(OnlineOrderKey),
    FOREIGN KEY (CarrierKey) REFERENCES DimShipmentCarrier(CarrierKey),
    FOREIGN KEY (ShipmentDateKey) REFERENCES DimDate(DateKey)
);