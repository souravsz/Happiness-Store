from django.urls import path 
from . import views

urlpatterns = [ 
    path('', views.HomePage, name="homepage"),
    path('Products', views.Products, name="products"),
    path('Login', views.Login, name="login"),
    path('Register', views.Register, name="register"),
    path('Logout', views.Logout,name="logout"),
    path('ProductDetail/<id>', views.ProductDetails ,name="productdetail"),
    path('Cart', views.cart ,name="cart"),
    path('AddtoCart', views.AddtoCart ,name="addtocart"),
    path('RemoveCartItem/<id>', views.RemoveCartItem ,name="RemoveCartItem")
]