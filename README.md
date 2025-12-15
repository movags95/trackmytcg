# TrackMyTCG - TCG Portfolio Management Platform

## Project Overview
Full-stack TCG (Trading Card Game) portfolio management and analytics platform for tracking sealed product investments.

**Tech Stack:**
- **Frontend:** Next.js 14+, React, TypeScript, Tailwind CSS, shadcn/ui, Recharts
- **Backend:** Django 5.x, Django REST Framework
- **Database:** PostgreSQL
- **Auth:** Single hardcoded user (no authentication in MVP)

## Current Implementation Status

### Backend (Django) - PARTIALLY COMPLETE

#### Completed:
1. **Project Setup**
   - Django project initialized
   - PostgreSQL database configured
   - Django REST Framework and CORS configured
   - 5 Django apps created:
     - `apps.core` - Master data (TCG, Set, ProductType, Product)
     - `apps.transactions` - Purchase, Sale, Opening transactions
     - `apps.settings_app` - User settings
     - `apps.analytics` - Analytics calculations (TODO)
     - `apps.inventory` - Inventory calculations (TODO)

2. **Database Models**
   - ✅ Core models: TCG, ProductType, Set, Product
   - ✅ Transaction models: Purchase, PurchaseLineItem, Sale, SaleLineItem, Opening, OpeningLineItem
   - ✅ Settings model: UserSettings
   - ✅ Migrations created

3. **API - Core App**
   - ✅ Serializers for TCG, ProductType, Set, Product
   - ✅ ViewSets with CRUD operations
   - ✅ Deletion protection for referenced entities
   - ✅ URL routing configured

4. **API - Transactions App**
   - ✅ Serializers for Purchase, Sale, Opening with nested line items
   - ⏳ ViewSets (TODO)
   - ⏳ URL routing (TODO)

#### TODO - Backend:
1. **Complete Transactions App**
   - Create views.py with ViewSets for Purchase, Sale, Opening
   - Create urls.py for routing
   - Add inventory validation before sales

2. **Settings App**
   - Create serializers and views for UserSettings
   - Create URL routing

3. **Inventory App**
   - Create `calculations.py` with inventory calculation logic
   - Implement inventory endpoint with derived metrics
   - Add search/filter/sort functionality

4. **Analytics App**
   - Create `calculations.py` with all PRD formulas:
     - Purchase totals
     - Average unit cost (with delivery fee allocation)
     - COGS, Profit, ROI calculations
     - Holding duration calculations
     - Unrealized inventory valuation
     - Break-even calculation
   - Create API endpoints for all metrics
   - Implement time-range filtering

5. **Main URL Configuration**
   - Wire up all app URLs in config/urls.py

6. **Database Setup**
   - Install and start PostgreSQL
   - Run migrations: `python manage.py migrate`
   - Create hardcoded user via data migration or management command
   - Create default user settings

7. **CSV Import/Export**
   - Add import/export endpoints for all entities
   - Create downloadable templates
   - Implement validation and error handling

### Frontend (Next.js) - NOT STARTED

#### TODO - Frontend:
1. **Project Initialization**
   - Initialize Next.js 14 with TypeScript and App Router
   - Install dependencies:
     - Tailwind CSS
     - shadcn/ui components
     - Recharts
     - Lucide icons
   - Configure Tailwind and create base layout

2. **API Client**
   - Create `lib/api.ts` with Axios or Fetch client
   - Create `lib/types.ts` with TypeScript interfaces matching backend models
   - Configure base URL: http://localhost:8000/api/

3. **Master Data Management**
   - Create pages for TCGs, Sets, ProductTypes, Products
   - Build reusable data table component with search/filter/sort
   - Create modal forms for CRUD operations
   - Add inline entity creation during transactions

4. **Transaction Recording**
   - Purchase recording page with multi-line items
   - Sales recording page with inventory autocomplete
   - Openings recording page
   - Transaction history pages with filters

5. **Inventory Page**
   - Display inventory with calculated metrics
   - Implement search/filter/sort
   - Add low stock highlighting
   - Listed/unlisted toggle functionality

6. **Dashboard**
   - Summary metrics cards
   - Charts (cashflow, sales activity, cumulative revenue, profit by TCG/Set)
   - Top products tables
   - Recent activity feed

7. **Settings Page**
   - Currency selector
   - Low stock threshold
   - Color pickers for highlights
   - Date range and aggregation defaults

8. **CSV Import/Export**
   - Upload CSV functionality
   - Download CSV and templates
   - Error display for import failures

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Backend Setup

1. **Install PostgreSQL and create database:**
   ```bash
   createdb trackmytcg
   ```

2. **Install Python dependencies:**
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create hardcoded user (create a management command or run in shell):**
   ```bash
   python manage.py shell
   ```
   ```python
   from django.contrib.auth.models import User
   from apps.settings_app.models import UserSettings

   # Create user
   user = User.objects.create_user(
       username='tcguser',
       email='user@trackmytcg.com',
       password='password123'
   )

   # Create default settings
   UserSettings.objects.create(user=user)
   ```

5. **Run development server:**
   ```bash
   python manage.py runserver
   ```

   Backend API will be available at: http://localhost:8000/api/

### Frontend Setup (Once Implemented)

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Run development server:**
   ```bash
   npm run dev
   ```

   Frontend will be available at: http://localhost:3000/

## API Endpoints (Planned)

### Core Endpoints
- `GET/POST /api/tcgs/` - List/Create TCGs
- `GET/PUT/DELETE /api/tcgs/{id}/` - Retrieve/Update/Delete TCG
- `GET/POST /api/product-types/` - List/Create Product Types
- `GET/PUT/DELETE /api/product-types/{id}/` - Retrieve/Update/Delete Product Type
- `GET/POST /api/sets/` - List/Create Sets (filter by ?tcg={id})
- `GET/PUT/DELETE /api/sets/{id}/` - Retrieve/Update/Delete Set
- `GET/POST /api/products/` - List/Create Products (filter by ?tcg={id}&set={id}&product_type={id})
- `GET/PUT/DELETE /api/products/{id}/` - Retrieve/Update/Delete Product

### Transaction Endpoints (TODO)
- `GET/POST /api/purchases/` - List/Create Purchases
- `GET/PUT/DELETE /api/purchases/{id}/` - Retrieve/Update/Delete Purchase
- `GET/POST /api/sales/` - List/Create Sales
- `GET/PUT/DELETE /api/sales/{id}/` - Retrieve/Update/Delete Sale
- `GET/POST /api/openings/` - List/Create Openings
- `GET/PUT/DELETE /api/openings/{id}/` - Retrieve/Update/Delete Opening

### Inventory Endpoints (TODO)
- `GET /api/inventory/` - List all inventory with calculated metrics
  - Supports search, filter, sort
  - Returns: product details, quantity, avg cost, avg ROI, last sale price, etc.

### Analytics Endpoints (TODO)
- `GET /api/analytics/summary/` - High-level summary metrics
- `GET /api/analytics/profit-by-product/` - Profit breakdown by product
- `GET /api/analytics/profit-by-set/` - Profit breakdown by set
- `GET /api/analytics/profit-by-tcg/` - Profit breakdown by TCG
- `GET /api/analytics/cashflow/` - Time series cashflow data
- `GET /api/analytics/sales-activity/` - Time series sales activity
- `GET /api/analytics/cost-breakdown/` - Breakdown of shipping, fees, tax

### Settings Endpoints (TODO)
- `GET/PUT /api/settings/` - Get/Update user settings

### CSV Endpoints (TODO)
- `POST /api/{entity}/import/` - Import CSV
- `GET /api/{entity}/export/` - Export CSV
- `GET /api/{entity}/template/` - Download CSV template

## Database Schema

See [PRD_SPECIFICATION.md](PRD_SPECIFICATION.md) Section 1.5 for complete schema.

## Key Calculation Rules (Per PRD)

1. **All calculations are derived, not stored**
2. **Delivery fee allocation:** Proportional to line item cost within purchase
3. **Cost basis:** Always use average unit cost (no FIFO/LIFO)
4. **Inventory:** Only count received purchases (status = "Received")
5. **Opened products:** Excluded from profit/ROI metrics
6. **Unrealized valuation:** Use rolling average of last sale prices

## Next Steps

1. Complete backend transaction views and URLs
2. Complete analytics and inventory calculation engines
3. Complete settings API
4. Set up and run PostgreSQL database
5. Create hardcoded user
6. Test all backend endpoints
7. Initialize Next.js frontend project
8. Build frontend components and pages
9. Integrate frontend with backend API
10. End-to-end testing

## Reference Documents

- **Product Specification:** [PRD_SPECIFICATION.md](PRD_SPECIFICATION.md)
- **Implementation Plan:** `.claude/plans/wiggly-waddling-kahn.md`
- **AI Guidelines:** [CLAUDE.md](CLAUDE.md)
