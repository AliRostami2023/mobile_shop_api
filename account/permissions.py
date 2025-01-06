from rest_framework import permissions


class IsAdminOrSelf(permissions.BasePermission):
    """
    اجازه دسترسی به ادمین‌ها برای دیدن همه پروفایل‌ها.
    کاربران عادی فقط می‌توانند پروفایل خودشان را ببینند.
    """
    
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return True
    

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return obj.user == request.user
    