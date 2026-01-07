from django.urls import path
from .views import (
    AddMemberAPI,
    ListMembersAPI,
    DeleteMemberAPI,
    RenewMemberAPI,
    ExpiringSoonAPI,
    MemberRenewalHistoryAPI
)

urlpatterns = [
    path('add/', AddMemberAPI.as_view()),
    path('list/', ListMembersAPI.as_view()),
    path('delete/<int:member_id>/', DeleteMemberAPI.as_view()),
    path('renew/<int:member_id>/', RenewMemberAPI.as_view()),
    path('expiring-soon/', ExpiringSoonAPI.as_view()),
    path('renewal-history/<int:member_id>/', MemberRenewalHistoryAPI.as_view()),
]
