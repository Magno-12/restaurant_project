from rest_framework import permissions

class BelongsToRestaurantPermission(permissions.BasePermission):
    """
    Permiso personalizado para verificar que los objetos pertenezcan al restaurante del usuario.
    """
    message = "No tiene permiso para acceder a recursos de este restaurante."

    def has_permission(self, request, view):
        # Verificar si el usuario está autenticado y tiene un restaurante asignado
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.restaurant or request.user.is_superadmin)
        )

    def has_object_permission(self, request, view, obj):
        # Si es superadmin, tiene acceso a todo
        if request.user.is_superadmin:
            return True
            
        # Verificar si el objeto tiene atributo restaurant
        if hasattr(obj, 'restaurant'):
            return obj.restaurant == request.user.restaurant
            
        # Para objetos que se relacionan a través de otra entidad (como OrderItem)
        if hasattr(obj, 'order') and hasattr(obj.order, 'table'):
            return obj.order.table.restaurant == request.user.restaurant
            
        # Para otros tipos de relaciones
        if hasattr(obj, 'table'):
            return obj.table.restaurant == request.user.restaurant
            
        return False
