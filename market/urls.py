from django.urls import path
from .views import ProductsListView, ProductCreateView,ProductEditView, SellsTransactionsView, ProductUpdateView, ProductsDeleteView,AddsTransactionsView
from . import views

urlpatterns = [
    path("", ProductsListView.as_view(), name="products-list"),
    path("update/<pk>", ProductUpdateView.as_view(template_name="market/product_update.html"), name="product-update"),
    path("add-product/", ProductCreateView.as_view(), name="product-create"),
    path("edit-product/", ProductEditView.as_view(), name="edit-product"),
    path("sells-transactions/", SellsTransactionsView.as_view(), name="sells-transactions"),
    path("adds-history", AddsTransactionsView.as_view(), name="adds-history"),
    path("create-order", views.OrderCreateView, name="create-order"),
    path("delete/<pk>", ProductsDeleteView.as_view(), name="product-delete"),
    path("register", views.register_request, name="register"),
]
