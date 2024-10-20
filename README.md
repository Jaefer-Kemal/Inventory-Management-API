# Inventory Management System (IMS) API

Welcome to the Inventory Management System (IMS) API documentation. This API is designed to manage sales, purchases, warehouses, products, and user accounts. It provides a robust solution for managing orders and tracking stock levels across multiple warehouses, with a focus on user roles like customers, employees, and administrators.

## Table of Contents

- [Inventory Management System (IMS) API](#inventory-management-system-ims-api)
  - [Table of Contents](#table-of-contents)
  - [Project\_Overview](#project_overview)
  - [Features](#features)
  - [Installation\_and\_Setup](#installation_and_setup)
    - [Prerequisites](#prerequisites)
    - [Local Setup](#local-setup)
  - [Authentication](#authentication)
    - [Example of authenticating:](#example-of-authenticating)
  - [API-Endpoints](#api-endpoints)
    - [Audit Log](#audit-log)
    - [Inventory](#inventory)
    - [Orders](#orders)
    - [Users](#users)
    - [Warehouse](#warehouse)
  - [Response\_Codes](#response_codes)
  - [Contributing](#contributing)
  - [License](#license)

---

## Project_Overview

The IMS API offers a comprehensive suite of endpoints for managing products, sales, purchases, warehouse inventory, and user accounts. The system supports:

- **Sales Order Management**: Track customer orders and manage order statuses.
- **Purchase Order Management**: Handle purchase orders from suppliers.
- **Warehouse Inventory Management**: Organize and transfer product stock between warehouses.
- **User Registration and Management**: Manage customers, employees, and suppliers.

This API is RESTful and supports CRUD (Create, Read, Update, Delete) operations for various resources.

---

## Features

- **Audit Log**: Track history for sales, purchases, and stock movements.
- **Inventory Management**: Manage products, categories, and stock levels.
- **Order Management**: Create and manage purchase and sales orders.
- **Warehouse Management**: Organize stock across multiple warehouses.
- **User Management**: Register and manage employees, suppliers, and customers.
- **Token-based Authentication**: Secure endpoints using JWT tokens.

---

## Installation_and_Setup

### Prerequisites

Before setting up the project, ensure you have the following installed on your system:

- Python 3.8 or above
- Django
- Django REST Framework
- PostgreSQL (or another preferred database)
- Heroku CLI (if deploying to Heroku)

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/Jaefer-Kemal/Inventory-Management-API.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```   

3. Configure your environment variables:
    - Create a `.env` file in the root directory with your secret keys, database configurations, and other settings.
4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser for admin access:
```bash
python manage.py createsuperuser
```

6. Start the server:
```bash
python manage.py runserver
```

## Authentication

This API uses **JWT (JSON Web Token)** for securing endpoints. To access most endpoints, you must first authenticate and receive an access token. You can get the access and refresh tokens via:

- **Obtain Token**: `/api/account/token/`
- **Refresh Token**: `/api/account/token/refresh/`

### Example of authenticating:


```bash
POST /api/account/token/ {   "username": "user",   "password": "password" }
```

This will return:

```json
{   "access": "your_access_token",   "refresh": "your_refresh_token" }
```

Use the access token in the `Authorization` header for subsequent requests:


```makefile
Authorization: Bearer your_access_token
```
---

## API-Endpoints

### Audit Log

|Name|URL|Description|Methods|
|---|---|---|---|
|**Purchase History**|`/api/auditlog/purchase-history/`|Get a list of all purchase order histories.|GET|
|**Purchase History Detail**|`/api/auditlog/purchase-history/<id>/`|Retrieve details of a specific purchase history.|GET|
|**Sales History**|`/api/auditlog/sales-history/`|Get a list of all sales order histories.|GET|
|**Sales History Detail**|`/api/auditlog/sales-history/<id>/`|Retrieve details of a specific sales history.|GET|
|**Stock History**|`/api/auditlog/stock-history/`|Get a list of all warehouse stock histories.|GET|
|**Stock History Detail**|`/api/auditlog/stock-history/<id>/`|Retrieve details of a specific stock history.|GET|

### Inventory

| Name                        | URL                                           | Description                             | Methods         |
| --------------------------- | --------------------------------------------- | --------------------------------------- | --------------- |
| **List Products**           | `/api/inventory/products/`                    | Get a list of all available products.   | GET, POST       |
| **Product Details**         | `/api/inventory/products/<id>/`               | Retrieve details of a specific product. | GET, PUT, PATCH |
| **Upload Product Images**   | `/api/inventory/products/<id>/upload-images/` | Upload product images.                  | POST            |
| **List Warehouse Stocks**   | `/api/inventory/warehouse-stocks/`            | Get a list of warehouse stocks.         | GET, POST       |
| **Warehouse Stock Details** | `/api/inventory/warehouse-stocks/<id>/`       | Retrieve details of a warehouse stock.  | GET, PATCH, PUT |
| **List Categories**         | `/api/inventory/categories/`                  | Get a list of all product categories.   | GET, POST       |
| **Product Transfer**        | `/api/inventory/product-transfer/`            | Transfer a product between warehouses.  | POST            |

### Orders

| Name                            | URL                                           | Description                             | Methods    |
| ------------------------------- | --------------------------------------------- | --------------------------------------- | ---------- |
| **List Purchase Orders**        | `/api/orders/purchase-orders/`                | Get a list of purchase orders.          | GET, POST  |
| **Purchase Order Details**      | `/api/orders/purchase-orders/<id>/`           | Retrieve details of a purchase order.   | GET, PATCH |
| **List Sales Orders**           | `/api/orders/sales-orders/`                   | Get a list of sales orders.             | GET, POST  |
| **Sales Order Details**         | `/api/orders/sales-orders/<id>/`              | Retrieve details of a sales order.      | GET, PATCH |
| **Add Items to Sales Order**    | `/api/orders/sales-orders/{id}/add-items/`    | Add items to a specific sales order.    | POST       |
| **Add Items to Purchase Order** | `/api/orders/purchase-orders/{id}/add-items/` | Add items to a specific purchase order. | POST       |

### Users

|Name|URL|Description|Methods|
|---|---|---|---|
|**Employee Registration**|`/api/account/register/employee/`|Register a new employee.|POST|
|**Supplier Registration**|`/api/account/register/supplier/`|Register a new supplier.|POST|
|**Customer Registration**|`/api/account/register/customer/`|Register a new customer.|POST|
|**List Users**|`/api/account/list/`|Get a list of all users.|GET|
|**Obtain Token**|`/api/account/token/`|Obtain a JWT token using credentials.|POST|
|**Refresh Token**|`/api/account/token/refresh/`|Refresh the access token using a refresh token.|POST|

### Warehouse

|Name|URL|Description|Methods|
|---|---|---|---|
|**List Warehouses**|`/api/warehouse/`|Get a list of all warehouses.|GET, POST|
|**Warehouse Details**|`/api/warehouse/<id>/`|Retrieve details of a specific warehouse.|GET, PUT, PATCH|
|**Warehouse Products**|`/api/warehouse/<id>/products/`|Get a list of all products in a specific warehouse.|GET|

---

## Response_Codes

- `200 OK`: The request was successful.
- `201 Created`: A new resource was successfully created.
- `400 Bad Request`: The request was invalid or cannot be served.
- `401 Unauthorized`: Authentication failed or user is not authenticated.
- `403 Forbidden`: The authenticated user is not allowed to access the resource.
- `404 Not Found`: The requested resource could not be found.
- `500 Internal Server Error`: The server encountered an unexpected condition.

---

## Contributing

We welcome contributions! If you would like to contribute to this project, please fork the repository and create a pull request. Ensure that your code follows the style guidelines and includes relevant tests.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.