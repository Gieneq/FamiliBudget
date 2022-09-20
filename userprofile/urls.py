from django.urls import path, include
from .views import UserListView, UserCreateView, user_detail_view, UserDeleteView, UserEditView, UserEditPasswordView
from .views import UserProfileListView, UserProfileDetailView, UserProfileDetailBudgetsView

app_name = 'userprofile'
# todo user cannot be names Profile, Add

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('add/', UserCreateView.as_view(), name='user_create'),
    path('profile/', UserProfileListView.as_view(), name='userprofile_list'),
    path('<slug:slug>/', user_detail_view, name='user_detail'),
    path('<slug:user_profile__slug>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('<slug:user_profile__slug>/edit/', UserEditView.as_view(), name='user_edit'),
    path('<slug:user_profile__slug>/pswd/', UserEditPasswordView.as_view(), name='user_editpassword'),
    path('profile/<slug:slug>/', UserProfileDetailView.as_view(), name='userprofile_detail'),
    path('profile/<slug:slug>/budgets/', UserProfileDetailBudgetsView.as_view(), name='userprofile_budget_detail'),
]
