from django.urls import path
from home.views import HomeView, ItemDetailVIew, SearchView, signup, add_to_cart, OrderSummaryView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('product/<slug>', ItemDetailVIew.as_view(), name = 'product'),
    path('search/', SearchView.as_view(), name = 'search'),
    path('signup/', signup,name = 'signup'),
    path('order/', OrderSummaryView.as_view(), name = 'order'),
    path('add-to-cart/<slug>', add_to_cart, name = 'add-to-cart'),
]

