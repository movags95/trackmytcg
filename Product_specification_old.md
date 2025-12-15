# PRODUCT SPECIFICATION

(Authoritative Source of Truth)

Purpose: TrackMyTCG is a definitive analytics and portfolio management platform for the Trading Card Game (TCG) ecosystem. It enables hobbyists and small-scale businesses to track, value, and analyze sealed TCG products with speed, accuracy, and clear investment insights.

This document overrides any assumptions by the AI.

### 1.1 Product Overview

Product Name:
TrackMyTCG

One-Sentence Description:
A 'One stop shop' personal investment ledger + analytics engine for sealed TCG products, optimized for accuracy, speed of input, and actionable insights.

Problem Statement:
I have recently picked up the hobby within the last 6 months and after investing around £4000 and have sold around half of my products for around 25% in returns. I have realised that TCG sealed products can be a lucrative market. However, as someone who also enjoys opening packs and the chase of finding the hit cards, it can also be expensive. In order to recoup my costs, I have sold some of my products for a decent margin. I have struggled to find a central location to track my business and my hobby at the same time. There are so many apps that track a TCG portfolio, however inputting all your data on these platforms can be quite slow and tedious. I also have found a few solutions that also allow you to record sales but the problem is that it doesnt give you those valuable insigts to show you what are the best performing products. I also cant track the value of my portfolio in realtime. I have also used a spreadsheet which is fine but also such a intensive way of storing data and performing metric caluclations is often complex and requires a deeper understanding of spreadsheets. 

Target Users:

Primary User: A Hobbyist, with no knowledge of code and is just looking for a platform to track thier porfolio of sealed products with the option to track individial cards if they wish. With simplicity, and the speed of the platform & data input at the core of their experience. 

Secondary User(s): A one-man business, with no knowledge of code and some knowlege of business and business metrics. A business that buys sealed TCG products and choses to keep (invest) or use third party tools like eBay to list and make their sales for small returns. They are also a hobbyist, so from time to time they may open some of their sealed collection prodcuts for personal use. They should be able to track personal use but not mix it up with their business metrics.

User Environment Assumptions:

Platform(s): Web / Desktop / Mobile-friendly

Devices: Mobile / Desktop / Tablet

Connectivity: Online-only / Offline support / Hybrid

### 1.2 Goals & Non-Goals
Goals (Strict)

G1: Accurately track all sealed product purchases, sales, and openings

G2: Automatically calculate profit, ROI, holding time, and inventory value

G3: Minimize human input errors

G4: Surface clear, actionable insights within seconds

G5: Replace spreadsheet workflows entirely

Non-Goals (Explicit)

NG1: No peer-to-peer selling

NG2: No automated buying/selling

NG3: No speculative price predictions (initial version)

NG4: No card-level tracking (sealed products only)

⚠️ Any feature not explicitly listed as a goal is considered out of scope.

### 1.3 Functional Requirements
#### Core Features
##### Feature 1: Purchase Tracking

Description:
Users must be able to record any purchases of sealed products with quick entry, minimal manual input and zero ambiguity. A purchase can contain multiple items. 

Inputs:

Product (controlled list)
TCG (eg. Pokemon, One Piece, Topps)
Set name (Phantasmal Flames)
Product Type (Booster pack)
Quantity
Unit cost
Purchase date
Vendor
Notes (optional)
Online order (boolean)
Delivery fee (if online order)
Status (Recieved, Preorder, Awaiting delivery)

System Rules:

Total cost = quantity × unit cost (calculated, not entered)
Product identifiers must be normalized
No free-text product naming without confirmation

##### Feature 2: Inventory management

Description:
The system must always reflect the exact number of sealed products currently held. Users can mark products as listed or unlisted for information purposes only. 

Rules:
Inventory increases only via purchases
Inventory decreases only via sales or openings
Inventory can never go negative
Opened products are permanently excluded from inventory
Any inventory that reaches zero, automatically is marked as unlisted


##### Feature 3: Recording Sales

Description:
Users must be able to record sales made against their sealed TCG inventory with quick entry, minimal manual input and zero ambiguity. A sale can be made up of mulitple products and/or quanitites.

Inputs:

Sale date
Platform (eBay, Private etc.)
Prodcut (reference from inventory)
Quantity sold
Unit sale price
Shipping payment by (buyer side or seller side - needs to be taken into account in calculations)
Shipping cost
Platform fees
Tax
Sale URL (optional)
Buyer username (optional)

System Calculations:
Gross revenue
Net revenue
Profit
ROI
Holding duration

##### Feature 4: Personal Use tracking

Description:
Track products opened for hobby purposes without polluting investment/sales metrics

Inputs:
Date opened
Product(s)
Quantity(ies)

Rules:
Opened products are removed from inventory
Cost basis is preserved
Opened products are excluded from ROI calculations

##### Feature 5: Insights and Analytics

Description:
Users should see the metrics and insights most useful to them clearly by using text colours, highlighting and visuals/charts. Metrics should be understood at a quick glance with options to drill down or filter. Users should be able to switch time time ranges

Mandatory Metrics:
Total invested
Total realized profit
Unrealized value
ROI per product
ROI per set
Average holding time

Insights Must Be:
Deterministic
Explainable
Traceable to raw data

##### Feature 6: TCG, Products, Product Types and Sets management

Description:
Users should be able to add or change information about products, product types, sets, and TCGs. Quick entry, minimal manual input and zero ambiguity are the key areas that the user should experience.

Inputs for TCG:
TCG name (eg. Pokemon)

Inputs for Product types:
Product type name (eg. Booster box)
Prodcut type code (eg. BB)
Default pack count (used to calculate average price per booster pack)

Input for Sets:
TCG (reference from TCG)
Set Name
Set Code

Input for Products
Set, Product type (referenced from their corresponding tables)
Product name
Pack count
Is listed (Boolean)

System rules:
A product is required to have a reference to a TCG, Set and Product type.
Product names are made up of the Set name and Product type by default (for speedy input) but not required to be adhered to.

##### Feature 7: Data import and export

Description:
Users should be able import and export data to the system. Formats should be .CSV.

System rules:
Data integrity must be maintained
Templates should be downloadable from the system

##### Feature 8: Persistant setting and app preferences

Description:
Users should be able to customize the app setting to tailor it to their preferences.

Global Settings:
Display currecny (GBP EUR USD)
Low stock level threshold (for low stock highlighting)
Highlight colour pickers for out of stock and low stock highlighting

Dashboard settings:
Date range
Time period

System rules:
Settings should persist every time the app is launched
Settings should be grouped with relavent settings


### 1.4 User Stories (Strict Format)
As a <specific user type>,
when I <specific action>,
the system MUST <specific outcome>,
so that <explicit benefit>.

Example:

As a first-time user,
when I submit the signup form with valid data,
the system MUST create an account and redirect me to onboarding,
so that I can start using the product immediately.

As a USER
when I make a purchase of sealed TCG products
the system MUST allow me to input all the relavent information for that transaction and store it for me, updating my inventory in the process
so that I can keep track of my spending and stock.

As a USER
When I make a purchase of a product where its TCG, Set, product type or product doesnt exist
the system MUST let me add the information for that product from the same screen
so that I can continue recording my purchase after adding the relevant details quickly and effectively.

As a USER
When I am viewing Product management
the system MUST let me add, edit or delete products while maintaining the integrity of the data
so that I do not accidentally delete products, TCGs, product types and/or sets that are being referenced throughout the system

As a USER
When looking at my inventory
The system must clearly highlight items that are running low on stock and that are out of stock. It should also show me average cost, average ROI, average price per pack, is listed and last sold price for each prodcut.
So that I can make quick checks when creating a listing on a desired platform. 

As a USER
When looking at my inventory
The system MUST allow me to search, filter and sort through products
So that I can manage my inventory easily and see my position easily. 

As a USER
When looking at my inventory
The system MUST allow me to mark selected products as listed or unlisted
So that I can see what products I currently have listed for sale.

As a USER
When making a purchase
The system must allow me to record multi-item transactions
So that I dont have fill out mulitple forms per product as I can input them in the same transaction

As a USER
When viewing my purchase history
The system must allow me to edit or delete entries
So that I can quickly correct any mistakes I might have made during data entry

As a USER 
When viewing my purchase history
The system MUST allow me to search, filter and/or sort through my purchases. By default purchases should be sorted by date in decending order
So that I can quickly find details of my most recent purchases first

As a USER
when looking at the purchases screen
The system must show me the products/purchases that do not have a status of 'Received'. In a compact manner with warning level styling
This is so that I can keep track of any products that I am still waiting for through a preorder or delievery

As a USER
When recording a sale
The system should allow me to input product details quickly by suggesting autofill as I type product name. 
This is so that I can fill out forms quickly

As a USER
When looking at my sales
The system MUST allow me to search, filter and/or sort through my sales. By default sales should be sorted by date in decending order
This is so that I can view sales data quickly

As a USER
When wishing to import data to the system via CSV file
The system should have an option to download templates for any data imports
This is so that when I import data, I have a clear template to work from

As a USER
When looking to export the data
The system must provide CSV extracts of all data entities. The CSV exports should be reimportable to the system.
This is so that, I can import and export data consistently from different versions of the app.

As a USER
When looking at metrics/dashboard
I want the following questions to be clearly answered:
    how much I have spent? (total and over time)
    how much I have sold? (total and over time)
    how much profit and ROI I have made of the products sold? (total and over time)
    how much profit do I need to make to break even?
    how many sales have I made and how much profit on average is each sale returning?
    how much of the revenue is being used towards delivery, tax and fees?
    what is my most profitable TCG/set/product type?
    what is the average cost per booster pack by TCG?
    what is my sales activity over time?
    what is my cashflow over time?
    what is my cumulative revenue over time?
    what products should I invest more money into?
    what products have been in the storeroom for too long?
This is so that I can make informed business and investment decisions

### 1.5 Data Requirements

### 1.6 API & Integration Requirements (If Applicable)

### 1.7 Performance Constraints

### 1.8 Acceptance Criteria (Mandatory)
