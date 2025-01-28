# Restaurant Management System API Documentation

## Índice
1. [Autenticación](#autenticación)
2. [Gestión de Mesas](#gestión-de-mesas)
3. [Gestión de Órdenes](#gestión-de-órdenes)
4. [Gestión de Platos](#gestión-de-platos)

## Autenticación

### Login
Inicia sesión en el sistema y obtiene un token JWT con duración de 24 horas.

**Endpoint:** `POST /api/v1/users/auth/login/`

**Request Body:**
```json
{
    "email": "user@restaurant.com",
    "password": "userpassword",
    "restaurant_code": "123456"  // Opcional en primer paso
}
```

**Response (200 OK):**
```json
{
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    },
    "user": {
        "id": 1,
        "email": "user@restaurant.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "waiter",
        "restaurant_code": "123456",
        "is_restaurant_admin": false,
        "is_superadmin": false
    },
    "requires_restaurant_code": true  // Solo si se requiere verificación adicional
}
```

### Verificar Código de Restaurante
Verifica el código del restaurante cuando se requiere en el proceso de login.

**Endpoint:** `POST /api/v1/users/auth/verify_restaurant_code/`

**Request Body:**
```json
{
    "code": "123456"
}
```

**Response (200 OK):**
```json
{
    "message": "Código verificado exitosamente",
    "restaurant": {
        "id": 1,
        "name": "Restaurant Name",
        "code": "123456"
    }
}
```

### Logout
Cierra la sesión y añade el token a la lista negra.

**Endpoint:** `POST /api/v1/users/auth/logout/`

**Request Body:**
```json
{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
    "message": "Sesión cerrada exitosamente"
}
```

## Gestión de Mesas

### Listar Mesas
Obtiene todas las mesas del restaurante con su estado actual.

**Endpoint:** `GET /api/v1/management/tables/`

**Response (200 OK):**
```json
{
    "count": 2,
    "results": [
        {
            "id": 1,
            "table_number": "1",
            "status": "available",
            "capacity": 4,
            "current_server_name": "John Doe",
            "occupied_since": null,
            "location": "Main Hall"
        },
        {
            "id": 2,
            "table_number": "2",
            "status": "occupied",
            "capacity": 6,
            "current_server_name": "Jane Smith",
            "occupied_since": "2025-01-28T14:30:00Z",
            "location": "Terrace"
        }
    ]
}
```

### Actualizar Estado de Mesa
Actualiza el estado de una mesa específica.

**Endpoint:** `PATCH /api/v1/management/tables/{id}/update_status/`

**Request Body:**
```json
{
    "status": "occupied"  // available, occupied, reserved, cleaning
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "table_number": "1",
    "status": "occupied",
    "capacity": 4,
    "current_server_name": "John Doe",
    "occupied_since": "2025-01-28T14:35:00Z",
    "location": "Main Hall"
}
```

## Gestión de Órdenes

### Crear Nueva Orden
Crea una nueva orden para una mesa.

**Endpoint:** `POST /api/v1/management/orders/create_order/`

**Request Body:**
```json
{
    "table_id": 1,
    "number_of_guests": 4
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "table": 1,
    "table_number": "1",
    "server": {
        "id": 1,
        "name": "John Doe"
    },
    "status": "open",
    "items": [],
    "subtotal": "0.00",
    "tax": "0.00",
    "total": "0.00",
    "payment_status": "pending"
}
```

### Añadir Item a Orden
Añade un plato a una orden existente.

**Endpoint:** `POST /api/v1/management/orders/{order_id}/add_item/`

**Request Body:**
```json
{
    "dish": 1,
    "quantity": 2,
    "notes": "Sin salsa, extra queso"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "dish": {
        "id": 1,
        "name": "Hamburguesa Clásica"
    },
    "quantity": 2,
    "unit_price": "15.99",
    "notes": "Sin salsa, extra queso",
    "status": "pending"
}
```

### Actualizar Estado de Item
Actualiza el estado de preparación de un item en la orden.

**Endpoint:** `PATCH /api/v1/management/orders/{order_id}/items/{item_id}/status/`

**Request Body:**
```json
{
    "status": "ready"  // pending, preparing, ready, served, cancelled
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "status": "ready",
    "updated_at": "2025-01-28T14:40:00Z"
}
```

### Procesar Pago
Procesa el pago de una orden y la marca como completada.

**Endpoint:** `POST /api/v1/management/orders/{order_id}/process_payment/`

**Request Body:**
```json
{
    "payment_method": "credit_card",  // credit_card, cash, bank_transfer
    "tip": "5.00"
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "status": "completed",
    "payment_status": "paid",
    "payment_method": "credit_card",
    "subtotal": "31.98",
    "tax": "3.20",
    "tip": "5.00",
    "total": "40.18",
    "completed_time": "2025-01-28T14:45:00Z"
}
```

## Gestión de Platos

### Listar Platos
Obtiene todos los platos disponibles, con opción de filtrar por categoría.

**Endpoint:** `GET /api/v1/management/dishes/`

**Query Parameters:**
- `category` (opcional): ID de la categoría
- `search` (opcional): Término de búsqueda

**Response (200 OK):**
```json
{
    "count": 2,
    "results": [
        {
            "id": 1,
            "name": "Hamburguesa Clásica",
            "description": "Carne de res, lechuga, tomate, queso cheddar",
            "price": "15.99",
            "available": true,
            "sale_price": "18.99",
            "tax_percentage": "10.00",
            "recipe_cost": "5.50",
            "profit_margin": "65.50"
        },
        {
            "id": 2,
            "name": "Ensalada César",
            "description": "Lechuga romana, crutones, parmesano, aderezo césar",
            "price": "12.99",
            "available": true,
            "sale_price": "14.99",
            "tax_percentage": "10.00",
            "recipe_cost": "4.00",
            "profit_margin": "69.20"
        }
    ]
}
```

### Obtener Modificadores de Plato
Obtiene las opciones de modificación disponibles para un plato.

**Endpoint:** `GET /api/v1/management/dishes/{dish_id}/modifiers/`

**Response (200 OK):**
```json
{
    "options": [
        {
            "id": 1,
            "name": "No Dressing",
            "price": 0
        },
        {
            "id": 2,
            "name": "Extra Dressing",
            "price": 1.00
        }
    ],
    "additions": [
        {
            "id": 1,
            "name": "Extra Cheese",
            "price": 2.00
        },
        {
            "id": 2,
            "name": "Add Avocado",
            "price": 2.50
        }
    ]
}
```

## Notas Importantes

1. **Autenticación**
   - Todos los endpoints (excepto login) requieren el token JWT en el header:
     ```
     Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
     ```
   - Los tokens expiran después de 24 horas.

2. **Permisos**
   - Cada usuario solo puede acceder a recursos de su restaurante asignado.
   - Los super administradores pueden acceder a todos los recursos.

3. **Manejo de Errores**
   - Todos los endpoints pueden retornar los siguientes códigos de error:
     - 400: Bad Request (datos inválidos)
     - 401: Unauthorized (no autenticado)
     - 403: Forbidden (sin permisos)
     - 404: Not Found (recurso no encontrado)
     - 500: Internal Server Error

4. **Paginación**
   - Las listas de recursos están paginadas por defecto (20 items por página).
   - Se pueden ajustar usando los parámetros `page` y `page_size`.

5. **Timestamps**
   - Todas las fechas y horas están en formato UTC ISO 8601.
   - Ejemplo: `"2025-01-28T14:30:00Z"`
