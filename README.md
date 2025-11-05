# GitHub Classroom Assignments for Final Year Students


## Assignment 3: Real-Time Inventory Management System

**Skills Tested:** Object Manipulation, State Management, Event Processing

**Difficulty:** Medium

### Problem Statement
Build an inventory management system that handles real-time stock updates, supplier management, and reorder logic.

### Requirements

1. **`processTransactions(inventory, transactions)`**
   - Apply batch of transactions (purchases, sales, returns)
   - Update inventory state atomically
   - Return updated inventory and transaction log
   - Validate: no negative stock, valid product IDs

2. **`getStockAlerts(inventory, thresholds)`**
   - Identify products below reorder points
   - Calculate days until stockout based on avg daily sales
   - Return prioritized alerts (critical, warning, info)

3. **`optimizeWarehouseLayout(inventory, warehouseZones)`**
   - Assign products to zones based on turnover rate
   - High-turnover items in accessible zones
   - Return object mapping product IDs to zone IDs
   - Minimize total "distance score"

4. **`reconcileInventory(systemInventory, physicalCount)`**
   - Compare system records vs physical count
   - Identify discrepancies (overages, shortages, mismatches)
   - Generate adjustment transactions
   - Calculate variance percentage

5. **`forecastRestockDate(productId, inventory, salesHistory)`**
   - Predict when product needs restocking
   - Use 30-day moving average for sales rate
   - Account for lead time and safety stock
   - Return date object or "RESTOCK NOW" if critical

### Sample Data Structure
```javascript
const inventory = {
  products: {
    "SKU001": {
      name: "Product A",
      quantity: 150,
      reorderPoint: 50,
      leadTimeDays: 7,
      location: "Zone-A"
    }
  }
};

const transactions = [
  { type: "SALE", productId: "SKU001", quantity: 10, timestamp: "2024-11-01T10:30:00Z" },
  { type: "PURCHASE", productId: "SKU001", quantity: 100, timestamp: "2024-11-01T14:00:00Z" }
];
```

### Evaluation Criteria
- **Data Integrity:** 30% - No invalid states created
- **Business Logic:** 30% - Correct calculations and predictions
- **Error Handling:** 20% - Graceful handling of edge cases
- **Documentation:** 20% - Clear JSDoc comments

## General Submission Guidelines for All Assignments

### Repository Structure
```
├── src/
│   ├── solution.js (or solution.py)
│   └── utils/ (helper functions)
├── tests/
│   └── solution.test.js
├── README.md (approach explanation)
├── COMPLEXITY.md (Big-O analysis)
└── package.json (or requirements.txt)
```

### Time Limit
- 60 minutes
