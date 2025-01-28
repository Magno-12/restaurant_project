# Restaurant Management System

## Estructura del Proyecto

El proyecto está organizado en aplicaciones Django separadas, cada una con una responsabilidad específica:

### 🔹 default
Aplicación base que contiene configuraciones y modelos compartidos.
- `models/`: Modelos base como BaseModel
- `admin.py`: Configuraciones de admin compartidas
- `apps.py`: Configuración de la aplicación

### 🔹 food
Gestión de alimentos, inventario e ingredientes.
- `models/`:
  - `ingredient.py`: Ingredientes base
  - `inventory.py`: Control de inventario
  - `inventory_ingredient.py`: Relación entre inventario e ingredientes
- `admin.py`: Interfaces de administración para alimentos
- `utils.py`: Utilidades y constantes (ej: CATEGORY_CHOICES)

### 🔹 management
Gestión operativa del restaurante.
- `models/`:
  - `restaurant.py`: Configuración del restaurante
  - `dish.py`: Platos y menús
  - `dish_ingredient.py`: Ingredientes por plato
  - `table.py`: Gestión de mesas
  - `order.py`: Sistema de pedidos
  - `employee.py`: Gestión de personal

### 🔹 users
Gestión de usuarios y autenticación.
- `models/`:
  - `user.py`: Modelo de usuario personalizado
- `utils.py`: Roles y permisos

## Flujo de Datos y Relaciones

### 1. Gestión de Restaurantes
```
Restaurant
├── Código único (6 dígitos)
├── Información básica (nombre, dirección, etc.)
└── Configuraciones (capacidad, horarios)
```

### 2. Sistema de Usuarios
```
User
├── Superadmin (gestión global)
├── Admin de Restaurante
└── Empleados
    ├── Meseros
    ├── Cocineros
    └── Cajeros
```

### 3. Gestión de Inventario
```
Inventory
├── Ingredientes
│   ├── Información básica
│   └── Costos
└── Stock
    ├── Cantidades
    └── Valores
```

### 4. Sistema de Menú
```
Dish
├── Información básica
├── Precios
└── Ingredientes
    ├── Cantidades
    └── Costos
```

## Panel de Administración

### 🔸 Superadmin
- Acceso: `admin@restaurantproject.com / SuperAdmin123!`
- Puede crear y gestionar restaurantes
- Acceso completo a todas las funcionalidades

### 🔸 Admin de Restaurante
- Acceso: `admin@[restaurante].com / Admin123!`
- Gestiona su restaurante específico
- Funcionalidades:
  - Gestión de empleados
  - Control de inventario
  - Configuración de menú
  - Gestión de mesas

### 🔸 Empleados
- Acceso: `[rol]@[restaurante].com / Employee123!`
- Acceso limitado según su rol

## Configuración del Admin

### Restaurant Admin
```python
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'capacity', 'is_active')
    search_fields = ('name', 'code')
```

### Inventory Admin
```python
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'restaurant', 'quantity', 'available_quantity')
    list_filter = ('restaurant', 'category')
```

### Dish Admin
```python
@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'available')
    inlines = [DishIngredientInline]
```

## Características por Módulo

### 1. Gestión de Inventario
- Control de stock por restaurante
- Seguimiento de ingredientes
- Alertas de nivel mínimo
- Cálculo automático de costos

### 2. Gestión de Menú
- Platos únicos por restaurante
- Cálculo automático de:
  - Costos de recetas
  - Precios con impuestos
  - Márgenes de beneficio

### 3. Gestión de Mesas
- Estados de mesa:
  - Disponible
  - Ocupada
  - Reservada
  - En limpieza
- Asignación de meseros
- Control de capacidad

### 4. Sistema de Pedidos
- Registro de órdenes
- Estados de pedido
- Cálculo de totales
- Gestión de pagos

## Scripts de Utilidad

### 1. Reset de Base de Datos
```bash
python clean_database.py
```
Limpia todas las tablas de la base de datos.

### 2. Reset de Migraciones
```bash
python reset_migrations.py
```
Reinicia todas las migraciones del proyecto.

### 3. Población de Datos
```bash
python populate_db.py
```
Crea datos de ejemplo incluyendo:
- Restaurantes
- Usuarios
- Inventario
- Menús
- Mesas

## Seguridad y Validaciones

1. **Separación por Restaurante**
   - Cada restaurante tiene sus propios:
     - Ingredientes
     - Inventario
     - Menú
     - Personal

2. **Validaciones de Datos**
   - Nombres únicos por restaurante
   - Códigos de restaurante únicos
   - Validación de pertenencia al mismo restaurante

3. **Control de Acceso**
   - Basado en roles
   - Restricciones por restaurante
   - Validación de permisos

## Consideraciones de Implementación

1. **Escalabilidad**
   - Modelos independientes por restaurante
   - Relaciones optimizadas
   - Índices en campos clave

2. **Mantenibilidad**
   - Estructura modular
   - Separación de responsabilidades
   - Código documentado

3. **Extensibilidad**
   - Fácil adición de nuevas funcionalidades
   - Modelos base reutilizables
   - Configuraciones flexibles
