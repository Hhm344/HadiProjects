# Event Management System (Database Project)

Database Systems course project, team of 3. Written in SQL (Microsoft SQL Server).

A relational database for running events: venues, organizers, events and their
sessions, speakers, ticket types, attendees, ticket sales, payments, and sponsors.

## What's included

- **Schema:** 12 tables with primary and foreign keys, including many-to-many
  tables for speakers per session (`PresentedBy`) and sponsors per event (`SponsoredBy`)
- **Sample data** for venues, events, sessions, tickets, and payments
- **20 queries**, for example:
  - total revenue per event
  - attendees whose payment is still pending
  - sponsors that support more than one event
  - events with no sponsors or no sessions
  - the best-selling ticket type for each event

The report also covers the ER/EER diagram, the relational schema, functional
dependencies, and relational algebra for selected queries.

## Tables

`Venue`, `Organizer`, `Sponsor`, `Event`, `TicketType`, `Session`,
`SessionSpeaker`, `PresentedBy`, `Attendee`, `Ticket`, `Payment`, `SponsoredBy`

## How to run

Open `EventManagement.sql` in SQL Server Management Studio (or Azure Data Studio)
and run it. It creates the tables, inserts the sample data, and runs the queries.
Queries 11 and 14 use `TOP 1`, which is SQL Server syntax.
