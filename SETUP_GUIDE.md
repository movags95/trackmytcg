# TrackMyTCG - Setup Guide

## Current Implementation Status

### Backend (Django) - COMPLETE ✅

The Django backend is fully implemented with all models, APIs, and calculation logic per the PRD specification.

#### Completed Components:

1. **Database Models** - All models created per PRD Section 1.5
   - Core models: TCG, ProductType, Set, Product
   - Transaction models: Purchase, PurchaseLineItem, Sale, SaleLineItem, Opening, OpeningLineItem
   - Settings model: UserSettings
   - Database migrations generated

2. **REST API Endpoints** - All CRUD operations implemented
   - `/api/tcgs/` - TCG management
   - `/api/product-types/` - Product type management
   - `/api/sets/` - Set management (with TCG filtering)
   - `/api/products/` - Product management (with multiple filters)
   - `/api/purchases/` - Purchase transactions with line items
   - `/api/sales/` - Sales transactions with line items
   - `/api/openings/` - Opening transactions with line items
   - `/api/inventory/` - Inventory with calculated metrics
   - `/api/analytics/summary/` - Dashboard summary metrics
   - `/api/analytics/profit-by-tcg/` - Profit breakdown by TCG
   - `/api/analytics/profit-by-set/` - Profit breakdown by Set
   - `/api/analytics/profit-by-product/` - Profit breakdown by Product
   - `/api/analytics/cashflow/` - Time series cashflow data
   - `/api/analytics/cost-breakdown/` - Shipping/fees/tax breakdown
   - `/api/settings/` - User settings management

3. **Calculation Engine** - All PRD formulas implemented
   - ✅ Purchase total cost calculation (Section 1.9.1)
   - ✅ Inventory quantity calculation (Section 1.9.2)
   - ✅ Average unit cost with delivery fee allocation (Section 1.9.3)
   - ✅ Sales calculations: gross/net revenue (Section 1.9.4)
   - ✅ Profit calculations with COGS (Section 1.9.5)
   - ✅ ROI calculations (Section 1.9.6)
   - ✅ Holding duration (Section 1.9.7)
   - ✅ Unrealized inventory valuation (Section 1.9.8)
   - ✅ Break-even calculation (Section 1.9.9)

4. **Data Integrity**
   - ✅ Referential integrity with PROTECT on deletes
   - ✅ Database indexes on foreign keys and filter fields
   - ✅ Status-based inventory counting (only RECEIVED purchases)
   - ✅ Proper handling of opened products (excluded from profit/ROI)

### Frontend (Next.js) - NOT STARTED ⏳

The frontend needs to be built from scratch. See Frontend Setup section below.

---

## Backend Setup Instructions

### Prerequisites

1. **PostgreSQL 14+** installed and running
2. **Python 3.11+** installed

### Step 1: Install PostgreSQL (if not already installed)

**Windows:**
- Download from https://www.postgresql.org/download/windows/
- Install with default settings
- Remember the postgres user password you set

**Mac:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Linux:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Create Database

Open PostgreSQL command line (psql) and run:

```sql
CREATE DATABASE trackmytcg;
```

Or from command line:

```bash
# Windows (assuming postgres user password is 'postgres')
psql -U postgres -c "CREATE DATABASE trackmytcg;"

# Mac/Linux
createdb trackmytcg
```

### Step 3: Update Database Credentials

If your PostgreSQL credentials differ from the defaults, update `backend/config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'trackmytcg',
        'USER': 'your_postgres_user',      # Update this
        'PASSWORD': 'your_postgres_password',  # Update this
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 4: Run Migrations

```bash
cd backend
./venv/Scripts/python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions, settings_app, transactions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying core.0001_initial... OK
  Applying transactions.0001_initial... OK
  Applying settings_app.0001_initial... OK
```

### Step 5: Create Hardcoded User

```bash
./venv/Scripts/python setup_database.py
```

This creates:
- Username: `tcguser`
- Email: `user@trackmytcg.com`
- Password: `password123`
- Default user settings

### Step 6: Run Development Server

```bash
./venv/Scripts/python manage.py runserver
```

Backend API will be available at: **http://localhost:8000/api/**

### Step 7: Test API (Optional)

You can test the API using curl or a tool like Postman:

```bash
# Test: Get all TCGs (should return empty array initially)
curl http://localhost:8000/api/tcgs/

# Test: Create a TCG
curl -X POST http://localhost:8000/api/tcgs/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Pokemon"}'

# Test: Get summary metrics
curl http://localhost:8000/api/analytics/summary/

# Test: Get inventory
curl http://localhost:8000/api/inventory/
```

---

## Frontend Setup Instructions

### Prerequisites

1. **Node.js 18+** and npm installed

### Step 1: Initialize Next.js Project

```bash
cd frontend
npx create-next-app@latest . --typescript --tailwind --app --eslint
```

When prompted:
- ✅ TypeScript: Yes
- ✅ ESLint: Yes
- ✅ Tailwind CSS: Yes
- ✅ `src/` directory: Yes
- ✅ App Router: Yes
- ❌ Import alias: No (or default)

### Step 2: Install Dependencies

```bash
npm install axios
npm install lucide-react
npm install recharts
npm install @tanstack/react-query
```

### Step 3: Install shadcn/ui

```bash
npx shadcn@latest init
```

When prompted, choose:
- Style: Default
- Base color: Slate (or preferred)
- CSS variables: Yes

Install required shadcn components:

```bash
npx shadcn@latest add button
npx shadcn@latest add input
npx shadcn@latest add label
npx shadcn@latest add table
npx shadcn@latest add dialog
npx shadcn@latest add select
npx shadcn@latest add card
npx shadcn@latest add dropdown-menu
npx shadcn@latest add form
npx shadcn@latest add toast
```

### Step 4: Create API Client

Create `frontend/src/lib/api.ts`:

```typescript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// TCGs
export const getTCGs = () => api.get('/tcgs/');
export const createTCG = (data: { name: string }) => api.post('/tcgs/', data);
export const updateTCG = (id: string, data: { name: string }) => api.put(`/tcgs/${id}/`, data);
export const deleteTCG = (id: string) => api.delete(`/tcgs/${id}/`);

// ... Add more API functions for other endpoints
```

### Step 5: Create TypeScript Types

Create `frontend/src/lib/types.ts`:

```typescript
export interface TCG {
  id: string;
  name: string;
}

export interface ProductType {
  id: string;
  name: string;
  code: string;
  default_pack_count: number | null;
}

// ... Add more types matching backend models
```

### Step 6: Run Development Server

```bash
npm run dev
```

Frontend will be available at: **http://localhost:3000/**

---

## API Documentation

### Core Endpoints

#### TCGs
- `GET /api/tcgs/` - List all TCGs
- `POST /api/tcgs/` - Create new TCG
- `GET /api/tcgs/{id}/` - Get TCG details
- `PUT /api/tcgs/{id}/` - Update TCG
- `DELETE /api/tcgs/{id}/` - Delete TCG (blocked if referenced)

#### Product Types
- `GET /api/product-types/` - List all product types
- `POST /api/product-types/` - Create new product type
- `GET /api/product-types/{id}/` - Get product type details
- `PUT /api/product-types/{id}/` - Update product type
- `DELETE /api/product-types/{id}/` - Delete product type (blocked if referenced)

#### Sets
- `GET /api/sets/` - List all sets
- `GET /api/sets/?tcg={tcg_id}` - List sets filtered by TCG
- `POST /api/sets/` - Create new set
- `GET /api/sets/{id}/` - Get set details
- `PUT /api/sets/{id}/` - Update set
- `DELETE /api/sets/{id}/` - Delete set (blocked if referenced)

#### Products
- `GET /api/products/` - List all products
- `GET /api/products/?tcg={tcg_id}&set={set_id}&product_type={type_id}` - Filtered list
- `POST /api/products/` - Create new product
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product (blocked if referenced)

### Transaction Endpoints

#### Purchases
- `GET /api/purchases/` - List all purchases
- `GET /api/purchases/?status={status}&start_date={date}&end_date={date}` - Filtered list
- `POST /api/purchases/` - Create new purchase with line items
- `GET /api/purchases/{id}/` - Get purchase details
- `PUT /api/purchases/{id}/` - Update purchase
- `DELETE /api/purchases/{id}/` - Delete purchase

**Purchase POST body example:**
```json
{
  "purchase_date": "2025-01-15",
  "vendor": "TCG Shop",
  "online_order": true,
  "delivery_fee": 5.00,
  "status": "RECEIVED",
  "notes": "January restock",
  "line_items": [
    {
      "product": "product-uuid-here",
      "quantity": 3,
      "unit_cost": 89.99
    }
  ]
}
```

#### Sales
- `GET /api/sales/` - List all sales
- `GET /api/sales/?platform={platform}&start_date={date}&end_date={date}` - Filtered list
- `POST /api/sales/` - Create new sale with line items
- `GET /api/sales/{id}/` - Get sale details
- `PUT /api/sales/{id}/` - Update sale
- `DELETE /api/sales/{id}/` - Delete sale

**Sale POST body example:**
```json
{
  "sale_date": "2025-01-20",
  "platform": "eBay",
  "shipping_paid_by": "BUYER",
  "shipping_cost": 10.00,
  "platform_fees": 12.50,
  "tax": 0.00,
  "sale_url": "https://ebay.com/item/123",
  "buyer_username": "pokemon_fan_123",
  "line_items": [
    {
      "product": "product-uuid-here",
      "quantity": 1,
      "unit_sale_price": 120.00
    }
  ]
}
```

#### Openings
- `GET /api/openings/` - List all openings
- `GET /api/openings/?start_date={date}&end_date={date}` - Filtered list
- `POST /api/openings/` - Create new opening with line items
- `GET /api/openings/{id}/` - Get opening details
- `DELETE /api/openings/{id}/` - Delete opening

### Inventory Endpoints

#### Get Inventory
- `GET /api/inventory/` - Get all inventory with calculated metrics
- Query parameters:
  - `search` - Search by product name, TCG, or set
  - `tcg` - Filter by TCG name
  - `stock_status` - Filter by `in_stock` or `out_of_stock`
  - `is_listed` - Filter by listed status (`true`/`false`)

**Response:**
```json
{
  "inventory": [
    {
      "product_id": "uuid",
      "product_name": "Pokemon Scarlet & Violet Booster Box",
      "tcg": "Pokemon",
      "set": "Scarlet & Violet",
      "product_type": "Booster Box",
      "quantity": 5,
      "average_cost": 89.50,
      "average_roi": 15.5,
      "price_per_pack": 2.49,
      "is_listed": true,
      "last_sale_price": 105.00,
      "pack_count": 36
    }
  ],
  "total_items": 1,
  "total_unrealized_value": 525.00
}
```

### Analytics Endpoints

#### Summary Metrics
- `GET /api/analytics/summary/` - Get all dashboard metrics

**Response:**
```json
{
  "total_invested": 5000.00,
  "total_realized_profit": 750.50,
  "unrealized_inventory_value": 2500.00,
  "overall_roi": 15.01,
  "break_even_revenue": 4249.50,
  "average_profit_per_sale": 37.53,
  "cost_breakdown": {
    "shipping": 200.00,
    "platform_fees": 150.25,
    "tax": 0.00,
    "total": 350.25
  }
}
```

#### Profit by TCG/Set/Product
- `GET /api/analytics/profit-by-tcg/?start_date={date}&end_date={date}`
- `GET /api/analytics/profit-by-set/?start_date={date}&end_date={date}`
- `GET /api/analytics/profit-by-product/?start_date={date}&end_date={date}`

#### Cashflow Time Series
- `GET /api/analytics/cashflow/?start_date={date}&end_date={date}&aggregation={daily|weekly|monthly}`

#### Cost Breakdown
- `GET /api/analytics/cost-breakdown/?start_date={date}&end_date={date}`

### Settings Endpoints

#### User Settings
- `GET /api/settings/` - Get user settings
- `PUT /api/settings/` - Update user settings

**Settings body:**
```json
{
  "currency": "GBP",
  "low_stock_threshold": 5,
  "highlight_low_stock_color": "#FFA500",
  "highlight_out_stock_color": "#FF0000",
  "default_date_range": "30d",
  "default_time_aggregation": "daily"
}
```

---

## Next Steps

1. ✅ Backend is complete
2. ⏳ Set up PostgreSQL database
3. ⏳ Run migrations and create hardcoded user
4. ⏳ Test backend API endpoints
5. ⏳ Initialize Next.js frontend
6. ⏳ Build UI components and pages
7. ⏳ Integrate frontend with backend API
8. ⏳ Add CSV import/export functionality (both backend and frontend)
9. ⏳ End-to-end testing

---

## Troubleshooting

### PostgreSQL Connection Issues

If you see: `connection to server at "localhost" (127.0.0.1), port 5432 failed`

**Solution:**
1. Check if PostgreSQL is running:
   ```bash
   # Windows
   services.msc  # Look for "postgresql" service

   # Mac
   brew services list

   # Linux
   sudo systemctl status postgresql
   ```

2. Start PostgreSQL if not running:
   ```bash
   # Windows: Start from Services or
   net start postgresql-x64-14

   # Mac
   brew services start postgresql@14

   # Linux
   sudo systemctl start postgresql
   ```

3. Verify connection:
   ```bash
   psql -U postgres -d trackmytcg
   ```

### Migration Errors

If migrations fail, try:
```bash
./venv/Scripts/python manage.py migrate --run-syncdb
```

### CORS Issues

If frontend can't connect to backend, ensure:
1. Django server is running on port 8000
2. Frontend is running on port 3000
3. CORS_ALLOWED_ORIGINS in settings.py includes `http://localhost:3000`

---

## File Structure Summary

```
trackmytcg/
├── backend/                     # Django backend (COMPLETE)
│   ├── apps/
│   │   ├── core/               # Master data models & APIs
│   │   ├── transactions/       # Purchase/Sale/Opening models & APIs
│   │   ├── analytics/          # Analytics calculations & APIs
│   │   ├── inventory/          # Inventory calculations & API
│   │   └── settings_app/       # User settings API
│   ├── config/                 # Django settings
│   ├── requirements.txt        # Python dependencies
│   └── setup_database.py       # User creation script
├── frontend/                    # Next.js frontend (TODO)
├── PRD_SPECIFICATION.md         # Product requirements
├── CLAUDE.md                    # AI execution guidelines
├── README.md                    # Project overview
└── SETUP_GUIDE.md              # This file
```

---

For questions or issues, refer to the PRD_SPECIFICATION.md for business logic details.
