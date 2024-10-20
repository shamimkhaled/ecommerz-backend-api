# from rest_framework.permissions import BasePermission

# class IsAdminOrHasRefundPermission(BasePermission):
#     """
#     Custom permission to only allow admins or users with 'can_process_refund' permission to process refunds.
#     """
#     message = 'You do not have permission to perform this action.'


#     def has_permission(self, request, view):
#         return request.user and (request.user.is_staff or request.user.has_perm('refund.can_process_refund'))
