from django.urls import path
from .views import ProductsListView, ProductCreateView,ProductEditView, SellsTransactionsView

urlpatterns = [
    path("", ProductsListView.as_view(), name="products-list"),
    path("add-product/", ProductCreateView.as_view(), name="product-create"),
    path("edit-product/", ProductEditView.as_view(), name="edit-product"),
    path("sells-transactions/", SellsTransactionsView.as_view(), name="sells-transactions"),
]
