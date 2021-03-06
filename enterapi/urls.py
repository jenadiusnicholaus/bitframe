
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from products.views import ProductListView, ProductCategories
from frame.views import FrameListView, GetFrameByAuthView

router = DefaultRouter()
router.register(r'framesList', FrameListView, basename='profile')
router.register(r'frame_by_auth', GetFrameByAuthView, basename='frame_by_auth')
router.register(r'products', ProductListView, basename='products')
router.register(r'product_categories', ProductCategories, basename='product_categories')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('user_auth/', include('authentication.urls')),
    path('product/', include('products.urls')),
    path('frame/',  include('frame.urls')),
    path('api/login_and_getToken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # base for future use
    path('', include(router.urls)),

]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)

