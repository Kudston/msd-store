from django.urls import path
from .views import ProductsListView, ProductCreateView,ProductEditView, SellsTransactionsView, ProductUpdateView, ProductsDeleteView

urlpatterns = [
    path("", ProductsListView.as_view(), name="products-list"),
    path("update/<pk>", ProductUpdateView.as_view(template_name="market/product_update.html"), name="product-update"),
    path("add-product/", ProductCreateView.as_view(), name="product-create"),
    path("edit-product/", ProductEditView.as_view(), name="edit-product"),
    path("sells-transactions/", SellsTransactionsView.as_view(), name="sells-transactions"),
    path("delete/<pk>", ProductsDeleteView.as_view(), name="product-delete"),
]
