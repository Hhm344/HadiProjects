--table creation for project

CREATE TABLE Venue (
    VenueID INT PRIMARY KEY,
    Name VARCHAR(100),
    Address VARCHAR(200),
    Capacity INT
);

CREATE TABLE Organizer (
    OrganizerID INT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(20)
);

CREATE TABLE Sponsor (
    SponsorID INT PRIMARY KEY,
    Name VARCHAR(100),
    ContactEmail VARCHAR(100)
);

CREATE TABLE Event (
    EventID INT PRIMARY KEY,
    Title VARCHAR(100),
    Description VARCHAR(300),
    StartDate DATE,
    EndDate DATE,
    VenueID INT,
    OrganizerID INT,
    FOREIGN KEY (VenueID) REFERENCES Venue(VenueID),
    FOREIGN KEY (OrganizerID) REFERENCES Organizer(OrganizerID)
);

CREATE TABLE TicketType (
    TicketTypeID INT PRIMARY KEY,
    EventID INT,
    Name VARCHAR(50),
    Price DECIMAL(10,2),
    QuantityAvailable INT,
    FOREIGN KEY (EventID) REFERENCES Event(EventID)
);

CREATE TABLE Session (
    SessionID INT PRIMARY KEY,
    EventID INT,
    Title VARCHAR(100),
    Room VARCHAR(50),
    StartTime TIME,
    EndTime TIME,
    FOREIGN KEY (EventID) REFERENCES Event(EventID)
);

CREATE TABLE SessionSpeaker (
    SpeakerID INT PRIMARY KEY,
    Name VARCHAR(100),
    ContactEmail VARCHAR(100)
);

CREATE TABLE PresentedBy (
    SessionID INT,
    SpeakerID INT,
    PRIMARY KEY (SessionID, SpeakerID),
    FOREIGN KEY (SessionID) REFERENCES Session(SessionID),
    FOREIGN KEY (SpeakerID) REFERENCES SessionSpeaker(SpeakerID)
);

CREATE TABLE Attendee (
    AttendeeID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    Phone VARCHAR(20)
);

CREATE TABLE Ticket (
    TicketID INT PRIMARY KEY,
    TicketTypeID INT,
    AttendeeID INT,
    PurchaseDate DATE,
    Status VARCHAR(20),
    FOREIGN KEY (TicketTypeID) REFERENCES TicketType(TicketTypeID),
    FOREIGN KEY (AttendeeID) REFERENCES Attendee(AttendeeID)
);

CREATE TABLE Payment (
    PaymentID INT PRIMARY KEY,
    TicketID INT,
    Amount DECIMAL(10,2),
    Method VARCHAR(50),
    PaymentDate DATE,
    Status VARCHAR(20),
    FOREIGN KEY (TicketID) REFERENCES Ticket(TicketID)
);

CREATE TABLE SponsoredBy (
    EventID INT,
    SponsorID INT,
    PRIMARY KEY (EventID, SponsorID),
    FOREIGN KEY (EventID) REFERENCES Event(EventID),
    FOREIGN KEY (SponsorID) REFERENCES Sponsor(SponsorID)
);

--Sample data

INSERT INTO Venue VALUES
(1, 'Grand Hall', 'Downtown Beirut', 500),
(2, 'Expo Center', 'Tripoli Main Road', 1200);

INSERT INTO Organizer VALUES
(1, 'hadi', 'hadi@example.com', '70000001'),
(2, 'hussein', 'hussein@example.com', '70000002');

INSERT INTO Sponsor VALUES
(1, 'Coca-Cola', 'contact@cocacola.com'),
(2, 'Samsung', 'events@samsung.com'),
(3, 'Bank of Beirut', 'info@bank.com');

INSERT INTO Event VALUES
(1, 'Tech Summit 2025', 'Technology & Innovation Expo', '2025-05-10', '2025-05-12', 1, 1),
(2, 'Music Festival', 'Live music and performances', '2025-08-20', '2025-08-21', 2, 2);

INSERT INTO TicketType VALUES
(1, 1, 'Standard', 30.00, 300),
(2, 1, 'VIP', 80.00, 100),
(3, 2, 'General Admission', 25.00, 500);

INSERT INTO Session VALUES
(1, 1, 'AI Workshop', 'Room A', '10:00', '12:00'),
(2, 1, 'Cybersecurity Talk', 'Room B', '13:00', '15:00'),
(3, 2, 'Live Band Performance', 'Main Stage', '18:00', '20:00');

INSERT INTO SessionSpeaker VALUES
(1, 'Dr. Sara jrab', 'sara123@gmail.com'),
(2, 'hadi muselmani', 'hhm86@gmail.com'),
(3, 'israa', 'israa123@gmail.com');

INSERT INTO PresentedBy VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO SponsoredBy VALUES
(1, 1),
(1, 2),
(2, 3);

INSERT INTO Attendee VALUES
(1, 'Ali', 'Hassan', 'ali@gmail.com', '76991234'),
(2, 'Maya', 'Sleiman', 'maya@gmail.com', '03445566'),
(3, 'Rami', 'Nasser', 'rami@gmail.com', '71223344');

INSERT INTO Ticket VALUES
(1, 1, 1, '2025-04-20', 'Paid'),
(2, 2, 2, '2025-04-22', 'Paid'),
(3, 3, 3, '2025-07-15', 'Pending');

INSERT INTO Payment VALUES
(1, 1, 30.00, 'Credit Card', '2025-04-20', 'Completed'),
(2, 2, 80.00, 'Cash', '2025-04-22', 'Completed'),
(3, 3, 25.00, 'Credit Card', '2025-07-15', 'Pending');



SELECT * FROM Event;
SELECT * FROM Ticket;
SELECT * FROM Payment;
SELECT * FROM Session;
SELECT * FROM PresentedBy;
SELECT * FROM SponsoredBy;
SELECT * FROM Attendee;


--Queries

-- q1: List all events along with the name of the venue where each event is held
SELECT Event.Title, Venue.Name AS VenueName
FROM Event
JOIN Venue ON Event.VenueID = Venue.VenueID;

-- q2: Retrieve all sessions (title, start time, end time) for EventID = 1
SELECT Session.Title, Session.StartTime, Session.EndTime
FROM Session
WHERE EventID = 1;

-- q3: Display all ticket types for each event along with their prices
SELECT Event.Title, TicketType.Name AS TicketType, TicketType.Price
FROM TicketType
JOIN Event ON TicketType.EventID = Event.EventID;

-- q4: Count the total number of tickets purchased for each event
SELECT Event.Title, COUNT(Ticket.TicketID) AS TicketsSold
FROM Ticket
JOIN TicketType ON Ticket.TicketTypeID = TicketType.TicketTypeID
JOIN Event ON TicketType.EventID = Event.EventID
GROUP BY Event.Title;

-- q5: Calculate the total revenue collected for each event from ticket payments
SELECT Event.Title, SUM(Payment.Amount) AS TotalRevenue
FROM Payment
JOIN Ticket ON Payment.TicketID = Ticket.TicketID
JOIN TicketType ON Ticket.TicketTypeID = TicketType.TicketTypeID
JOIN Event ON TicketType.EventID = Event.EventID
GROUP BY Event.Title;

-- q6: Show attendees who purchased tickets but whose payment status is still pending
SELECT Attendee.FirstName, Attendee.LastName, Ticket.TicketID
FROM Attendee
JOIN Ticket ON Attendee.AttendeeID = Ticket.AttendeeID
LEFT JOIN Payment ON Ticket.TicketID = Payment.TicketID
WHERE Payment.Status = 'Pending';

-- q7: List sponsors that support more than one event
SELECT Sponsor.Name, COUNT(*) AS SponsoredEvents
FROM SponsoredBy
JOIN Sponsor ON SponsoredBy.SponsorID = Sponsor.SponsorID
GROUP BY Sponsor.Name
HAVING COUNT(*) > 1;

-- q8: Retrieve all events organized by the organizer with OrganizerID = 1
SELECT Event.Title, Event.StartDate, Event.EndDate
FROM Event
JOIN Organizer ON Event.OrganizerID = Organizer.OrganizerID
WHERE Organizer.OrganizerID = 1;

-- q9: List all speakers who are presenting at the event with EventID = 2
SELECT Speaker.SpeakerID, Speaker.Name
FROM Session
JOIN PresentedBy ON Session.SessionID = PresentedBy.SessionID
JOIN SessionSpeaker AS Speaker ON PresentedBy.SpeakerID = Speaker.SpeakerID
WHERE Session.EventID = 2;

-- q10: Retrieve the attendees who purchased VIP tickets
SELECT FirstName, LastName
FROM Attendee
WHERE AttendeeID IN (
    SELECT AttendeeID
    FROM Ticket
    WHERE TicketTypeID IN (
        SELECT TicketTypeID
        FROM TicketType
        WHERE Name = 'VIP'
    )
);

-- q11: Find the event that has sold the highest number of tickets
SELECT TOP 1 E.Title, COUNT(T.TicketID) AS TicketsSold
FROM Ticket T
JOIN TicketType TT ON T.TicketTypeID = TT.TicketTypeID
JOIN Event E ON TT.EventID = E.EventID
GROUP BY E.Title
ORDER BY TicketsSold DESC;

-- q12: Show all events that do not have any sponsors
SELECT Title
FROM Event E
WHERE NOT EXISTS (
    SELECT 1 FROM SponsoredBy S WHERE S.EventID = E.EventID
);

-- q13: List attendees who have never purchased a ticket
SELECT A.FirstName, A.LastName
FROM Attendee A
WHERE NOT EXISTS (
    SELECT 1 FROM Ticket T WHERE T.AttendeeID = A.AttendeeID
);

-- q14: Identify the ticket type that generated the highest total revenue
SELECT TOP 1 TT.Name AS TicketType, SUM(P.Amount) AS Revenue
FROM Payment P
JOIN Ticket T ON P.TicketID = T.TicketID
JOIN TicketType TT ON T.TicketTypeID = TT.TicketTypeID
GROUP BY TT.Name
ORDER BY Revenue DESC;

-- q15: Show all sessions that take place between 10:00 and 14:00
SELECT Title, StartTime, EndTime
FROM Session
WHERE StartTime BETWEEN '10:00:00' AND '14:00:00';

-- q16: Retrieve all events sponsored by SponsorID = 1
SELECT E.EventID, E.Title, E.StartDate, E.EndDate
FROM Event E
JOIN SponsoredBy SB ON E.EventID = SB.EventID
WHERE SB.SponsorID = 1;

-- q17: List all events that are held at 'Grand Hall'
SELECT E.EventID, E.Title AS EventTitle, E.StartDate, V.Name AS VenueName
FROM Event E
JOIN Venue V ON E.VenueID = V.VenueID
WHERE V.Name = 'Grand Hall';

-- q18: Find all speakers who are participating in more than one session
SELECT S.SpeakerID, S.Name AS SpeakerName, COUNT(P.SessionID) AS TotalSessions
FROM SessionSpeaker S
JOIN PresentedBy P ON S.SpeakerID = P.SpeakerID
GROUP BY S.SpeakerID, S.Name
HAVING COUNT(P.SessionID) > 1;

-- q19: Show, for each event, which ticket type generated the highest total revenue
SELECT E.EventID, E.Title AS EventTitle, TT.TicketTypeID, TT.Name AS TicketType,
       SUM(P.Amount) AS TotalRevenue
FROM TicketType TT
JOIN Ticket T ON TT.TicketTypeID = T.TicketTypeID
JOIN Payment P ON T.TicketID = P.TicketID
JOIN Event E ON TT.EventID = E.EventID
GROUP BY E.EventID, E.Title, TT.TicketTypeID, TT.Name
ORDER BY TotalRevenue DESC;

-- q20: Display all events that currently have no sessions assigned
SELECT E.EventID, E.Title AS EventTitle
FROM Event E
LEFT JOIN Session S ON E.EventID = S.EventID
WHERE S.SessionID IS NULL;
