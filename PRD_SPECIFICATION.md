# PRODUCT SPECIFICATION

(Authoritative Source of Truth)

Purpose: TrackMyTCG is a definitive analytics and portfolio management platform for the Trading Card Game (TCG) ecosystem. It enables hobbyists and small-scale businesses to track, value, and analyze sealed TCG products with speed, accuracy, and clear investment insights.

This document supersedes the previous version of Product_specification.md and resolves ambiguities, gaps, and internal inconsistencies.

---

## 1.1 Product Overview

**Product Name:**  
TrackMyTCG

**One-Sentence Description:**  
A single, centralized investment ledger and analytics platform for sealed TCG products, optimized for fast data entry, deterministic calculations, and actionable insights.

**Problem Statement (Refined):**  
TCG collectors and small investors often operate simultaneously as hobbyists and resellers. Existing tools either focus on card-level portfolios, lack sales analytics, or require slow, error-prone manual input. Spreadsheets provide flexibility but demand advanced knowledge and significant maintenance. There is no single platform that cleanly separates personal hobby activity from investment performance while providing real-time portfolio valuation and clear ROI metrics for sealed TCG products.

**Target Users:**

- **Primary User:** Hobbyist collectors with no coding or advanced financial knowledge who want a fast, simple way to track sealed product purchases, inventory, and value, with optional personal-use tracking.
- **Secondary User:** Solo operators / micro-businesses buying and selling sealed TCG products for profit, who require sales tracking, ROI metrics, and business-grade insights without mixing personal hobby usage into financial reporting.

**User Model:**
- One user account represents a single portfolio
- No multi-user collaboration or multi-portfolio support in v1

**User Environment Assumptions (Clarified):**
- Platforms: Web application (responsive)
- Devices: Desktop, tablet, mobile
- Connectivity: Online-only (no offline mode in initial version)

---

## 1.2 Goals & Non-Goals

### Goals (Strict)
- G1: Accurately track all sealed product purchases, sales, and openings
- G2: Automatically calculate profit, ROI, holding duration, and inventory value
- G3: Minimize manual input and human error via controlled inputs and defaults
- G4: Surface deterministic, explainable insights within seconds
- G5: Fully replace spreadsheet-based workflows

### Non-Goals (Explicit)
- NG1: Peer-to-peer marketplace or listings
- NG2: Automated buying or selling
- NG3: Predictive or speculative price forecasting (v1)
- NG4: Card-level tracking (sealed products only)

Any feature not explicitly listed above is out of scope.

---

## 1.3 Functional Requirements

### Feature 1: Purchase Tracking

**Description:**  
Users can record purchases of sealed products via a single transaction containing multiple line items.

**Inputs (Per Line Item):**
- TCG (controlled list)
- Set (controlled list, filtered by TCG)
- Product type (controlled list)
- Product (controlled list)
- Quantity (integer > 0)
- Unit cost (numeric > 0)

**Inputs (Per Transaction):**
- Purchase date
- Vendor
- Online order (boolean)
- Delivery fee (optional, numeric ≥ 0)
- Status: Preorder | Awaiting Delivery | Received
- Notes (optional)

**System Rules:**
- Total cost = Σ(quantity × unit cost) + delivery fee
- Inventory increases only when status = Received
- Product identifiers must be normalized and reference existing entities

---

### Feature 2: Inventory Management

**Description:**  
Inventory represents only sealed products currently held.

**Rules:**
- Inventory increases only via received purchases
- Inventory decreases only via recorded sales or openings
- Inventory can never be negative
- Opened products are permanently removed from inventory
- Products with zero quantity are automatically marked as unlisted

---

### Feature 3: Sales Recording

**Description:**  
Users can record sales against existing inventory. One sale may include multiple products.

**Inputs:**
- Sale date
- Platform (e.g., eBay, Private)
- Product (inventory reference)
- Quantity sold
- Unit sale price *(in system currency)*
- Shipping paid by: Buyer | Seller
- Shipping cost
- Platform fees
- Tax *(informational, included in net calculations)*
- Sale URL (optional)
- Buyer username (optional)

**System Calculations:**
- Gross revenue
- Net revenue *(gross revenue minus shipping, platform fees, and tax)*
- Profit
- ROI
- Holding duration (purchase date → sale date)

---

### Feature 4: Personal Use Tracking

**Description:**  
Tracks products opened for hobby purposes without affecting financial performance metrics.

**Rules:**
- Opened products are removed from inventory
- Cost basis is retained for historical accuracy
- Opened quantities are excluded from profit, ROI, and sales metrics

---

### Feature 5: Insights & Analytics

**Mandatory Metrics:**
- Total invested
- Total realized profit
- Unrealized inventory value *(calculated using rolling average of last sale price per product)*
- ROI per product
- ROI per set
- Average holding duration

**Valuation Rules:**
- Unrealized inventory value is calculated using the average unit sale price from the most recent sales of the same product
- If no sales exist for a product, unrealized value is reported as 0 and flagged as "No market data"
- External market price feeds are explicitly out of scope for v1 but may replace or augment this logic in future versions

**Rules:**
- All metrics must be traceable to raw transactions
- No inferred or predictive data
- Time-range filtering required

---

### Feature 6: Master Data Management

**Entities:**
- TCG
- Product Type
- Set
- Product

**Key Rules:**
- Products must reference a TCG, Set, and Product Type
- Deletion is blocked if an entity is referenced by transactions
- Default product names are auto-generated but editable

---

### Feature 7: Data Import & Export

**Description:**  
CSV-based import and export for all major entities.

**Rules:**
- Import templates must be downloadable
- Exported CSVs must be re-importable without modification
- Referential integrity must be enforced

---

### Feature 8: Persistent Settings

**Global Settings:**
- Display currency (GBP, EUR, USD)
- Low stock threshold
- Highlight colors (low stock / out of stock)

**Currency Rules:**
- All transactions must be recorded in the currency defined in settings
- Mixed-currency transactions are not permitted
- Currency changes do not retroactively convert historical data

**Dashboard Settings:**
- Default date range
- Default time aggregation

Settings persist across sessions.

---

## 1.4 User Stories (Authoritative)

All user stories follow the strict format below and are considered mandatory requirements.

---

As a **USER**,  
when I make a purchase of sealed TCG products,  
the system MUST allow me to input all relevant transaction details and store them while updating my inventory accordingly,  
so that I can accurately track my spending and stock levels.

---

As a **USER**,  
when I make a purchase where the TCG, Set, Product Type, or Product does not yet exist,  
the system MUST allow me to create the missing entities from the same screen,  
so that I can continue recording my purchase without interruption.

---

As a **USER**,  
when I am managing products,  
the system MUST allow me to add, edit, or delete entities while preventing deletion of any entity that is referenced elsewhere,  
so that data integrity is always maintained.

---

As a **USER**,  
when I view my inventory,  
the system MUST clearly highlight low-stock and out-of-stock products and display average cost, average ROI, average price per pack, listed status, and last sale price,  
so that I can make quick and informed listing decisions.

---

As a **USER**,  
when viewing my inventory,  
the system MUST allow me to search, filter, and sort products,  
so that I can efficiently manage and understand my current position.

---

As a **USER**,  
when viewing my inventory,  
the system MUST allow me to mark products as listed or unlisted,  
so that I can track which products are actively for sale.

---

As a **USER**,  
when recording a purchase,  
the system MUST support multi-item transactions within a single purchase record,  
so that I do not need to submit multiple forms for the same transaction.

---

As a **USER**,  
when viewing my purchase history,  
the system MUST allow me to edit or delete purchase records,  
so that I can correct data entry errors.

---

As a **USER**,  
when viewing my purchase history,  
the system MUST allow me to search, filter, and sort purchases, with the default sort being most recent first,  
so that I can quickly locate relevant transactions.

---

As a **USER**,  
when viewing purchases,  
the system MUST clearly surface purchases that are not yet marked as "Received" using warning-level styling,  
so that I can track outstanding preorders and deliveries.

---

As a **USER**,  
when recording a sale,  
the system MUST provide fast product lookup via autocomplete against my inventory,  
so that I can enter sales data quickly and accurately.

---

As a **USER**,  
when viewing my sales history,  
the system MUST allow me to search, filter, and sort sales with the default sort being most recent first,  
so that I can review my sales performance efficiently.

---

As a **USER**,  
when importing data via CSV,  
the system MUST provide downloadable templates for each supported entity,  
so that imports can be performed correctly.

---

As a **USER**,  
when exporting data,  
the system MUST provide CSV exports for all major entities that can be re-imported without modification,  
so that my data remains portable across app versions.

---

As a **USER**,  
when viewing the dashboard and metrics,  
the system MUST clearly answer the following questions:
- Total spend (overall and over time)
- Total sales (overall and over time)
- Total profit and ROI on sold products
- Break-even point
- Average profit per sale
- Cost breakdown of shipping, tax, and fees
- Most profitable TCG, set, and product type
- Average cost per booster pack by TCG
- Sales activity over time
- Cashflow over time
- Cumulative revenue over time
- Products to reinvest in
- Products held for excessive durations

so that I can make informed business and investment decisions.

---

## 1.5 Data Requirements

### 1.5.1 Normalised Data Model

The system uses a fully normalised relational data model. All derived values are calculated, not stored, unless explicitly noted.

---

#### Users

| Field | Type | Notes |
|-----|-----|------|
| id | UUID | Primary key |
| email | string | Unique |
| created_at | datetime | |

---

#### TCGs

| Field | Type | Notes |
|-----|-----|------|
| id | UUID | Primary key |
| name | string | Unique |

---

#### ProductTypes

| Field | Type | Notes |
|-----|-----|------|
| id | UUID | Primary key |
| name | string | e.g. Booster Box |
| code | string | e.g. BB |
| default_pack_count | integer | Optional |

---

#### Sets

| Field | Type | Notes |
|-----|-----|------|
| id | UUID | Primary key |
| tcg_id | UUID | FK → TCGs |
| name | string | |
| code | string | |

---

#### Products

| Field | Type | Notes |
|-----|-----|------|
| id | UUID | Primary key |
| tcg_id | UUID | FK → TCGs |
| set_id | UUID | FK → Sets |
| product_type_id | UUID | FK → ProductTypes |
| name | string | Editable |
| pack_count | integer | |
| is_listed | boolean | Informational |

---

#### Purchases

| Field | Type | Notes |
|-----|-----|------|
| id | UUID | Primary key |
| user_id | UUID | FK → Users |
| purchase_date | date | |
| vendor | string | |
| delivery_fee | decimal | Default 0 |
| status | enum | Preorder / Awaiting / Received |
| notes | text | Optional |

---

#### PurchaseLineItems

| Field | Type | Notes |
|-----|-----|------|
| id | UUID | Primary key |
| purchase_id | UUID | FK → Purchases |
| product_id | UUID | FK → Products |
| quantity | integer | >0 |
| unit_cost | decimal | |

---

#### Sales

| Field | Type | Notes |
|-----|-----|------|
| id | UUID | Primary key |
| user_id | UUID | FK → Users |
| sale_date | date | |
| platform | string | |
| shipping_paid_by | enum | Buyer / Seller |
| shipping_cost | decimal | |
| platform_fees | decimal | |
| tax | decimal | Informational |
| sale_url | string | Optional |
| buyer_username | string | Optional |

---

#### SaleLineItems

| Field | Type | Notes |
|-----|-----|------|
| id | UUID | Primary key |
| sale_id | UUID | FK → Sales |
| product_id | UUID | FK → Products |
| quantity | integer | >0 |
| unit_sale_price | decimal | |

---

#### Openings

| Field | Type | Notes |
|-----|-----|------|
| id | UUID | Primary key |
| user_id | UUID | FK → Users |
| opened_date | date | |

---

#### OpeningLineItems

| Field | Type | Notes |
|-----|-----|------|
| id | UUID | Primary key |
| opening_id | UUID | FK → Openings |
| product_id | UUID | FK → Products |
| quantity | integer | >0 |

---

#### Settings

| Field | Type | Notes |
|-----|-----|------|
| user_id | UUID | PK / FK → Users |
| currency | enum | GBP / EUR / USD |
| low_stock_threshold | integer | |
| highlight_low_stock_color | string | |
| highlight_out_stock_color | string | |
| default_date_range | string | |
| default_time_aggregation | string | |

---

### 1.5.2 Derived Data (Not Persisted)

- Inventory quantity per product
- Average unit cost
- Average unit sale price (rolling)
- Unrealized inventory value
- Profit and ROI
- Holding duration

All derived data must be reproducible from transactional tables.

---

## 1.6 API & Integration Requirements

- Internal REST or equivalent API
- No third-party marketplace integrations in v1

---

## 1.7 Performance Constraints (Added)

- Dashboard load: < 2 seconds for up to 10,000 transactions
- Search/filter responses: < 500ms

---

## 1.8 Acceptance Criteria (Added)

- Inventory always reconciles with purchases, sales, and openings
- No calculation discrepancies between UI and stored data
- CSV imports reject invalid or incomplete rows with explicit errors
- All metrics are reproducible from raw data

---

## 1.9 Calculation Specification (Authoritative)

This section defines all financial and analytical calculations used by the system. All calculations are deterministic and derived exclusively from normalized transactional data. No calculated values are persisted unless explicitly stated.

---

### 1.9.1 Purchase Calculations

**Line Item Total Cost**  
`line_item_cost = quantity × unit_cost`

**Purchase Total Cost**  
`purchase_total_cost = Σ(line_item_cost) + delivery_fee`

Notes:
- Delivery fee is applied once per purchase
- Purchase costs do not affect inventory until purchase status = "Received"

---

### 1.9.2 Inventory Quantity Calculation

For a given product:

`inventory_quantity = received_purchases − sold_quantity − opened_quantity`

Where:
- `received_purchases` = sum of quantities from purchase line items with status = Received
- `sold_quantity` = sum of quantities from sale line items
- `opened_quantity` = sum of quantities from opening line items

Inventory quantity must never be negative.

---

### 1.9.3 Cost Basis Calculations

**Average Unit Cost (per product)**  
`average_unit_cost = total_received_cost ÷ total_received_quantity`

Where:
- `total_received_cost` includes proportional delivery fee allocation across line items
- Delivery fee allocation is proportional to line item cost within the purchase

---

### 1.9.4 Sales Calculations

**Gross Revenue (per sale)**  
`gross_revenue = Σ(quantity × unit_sale_price)`

**Net Revenue (per sale)**  
`net_revenue = gross_revenue − shipping_cost − platform_fees − tax`

---

### 1.9.5 Profit Calculations

**Cost of Goods Sold (COGS)**  
`COGS = quantity_sold × average_unit_cost`

**Profit (per sale)**  
`profit = net_revenue − COGS`

Notes:
- FIFO or LIFO is not used in v1
- Average cost basis is always applied

---

### 1.9.6 ROI Calculations

**ROI (per sale)**  
`ROI = (profit ÷ COGS) × 100`

**Aggregated ROI**  
Calculated as total profit ÷ total COGS for the aggregation scope.

---

### 1.9.7 Holding Duration

**Holding Duration (per unit sold)**  
`holding_days = sale_date − purchase_date`

Rules:
- When multiple purchase dates exist, use weighted average purchase date based on quantities
- Reported in days

---

### 1.9.8 Unrealized Inventory Valuation

**Average Unit Sale Price (rolling)**  
Calculated from the most recent sale line items per product.

**Unrealized Value (per product)**  
`unrealized_value = inventory_quantity × average_unit_sale_price`

Rules:
- If no sales exist for a product, unrealized value = 0
- Such products must be flagged as "No market data"

---

### 1.9.9 Break-Even Calculation

**Break-Even Revenue**  
`break_even = total_invested − total_realized_profit`

If value ≤ 0, portfolio is considered break-even or profitable.

---

### 1.9.10 Exclusions

- Opened products are excluded from profit, ROI, and holding calculations
- Inventory valuation never includes opened quantities
- Tax has no regional logic and is informational only

