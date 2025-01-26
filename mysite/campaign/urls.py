from django.urls import path
from campaign import views

app_name = "campaign"

urlpatterns = [
    path("", views.CampaignListView.as_view(), name="campaign-list"),
    path("<int:pk>/", views.CampaignDetailView.as_view(), name="campaign-detail"),
    path("create/", views.CampaignCreateView.as_view(), name="campaign-create"),
    path("update/<int:pk>/", views.CampaignUpdateView.as_view(), name="campaign-update"),
    path("delete/<int:pk>/", views.CampaignDeleteView.as_view(), name="campaign-delete"),
]
