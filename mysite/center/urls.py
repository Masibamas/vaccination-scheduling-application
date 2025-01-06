from django.urls import path
from center import views


app_name = "center"

urlpatterns = [
    path("", views.center_list, name="list"),
    path("<int:id>/", views.center_detail, name="detail"),
    path("create/", views.create_center, name="create"),
    path('update/<int:id>/', views.update_center, name="update"),
    path("delete/<int:id>/", views.delete_center, name="delete"),
]
