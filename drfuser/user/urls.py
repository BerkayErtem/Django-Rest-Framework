from django.urls import include, path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls import handler404



router=DefaultRouter()


router.register('register', userViewSet)
router.register('company',companyViewSet)
router.register('subsidiary', subsidiaryViewSet)
router.register('image', imageViewSet)
router.register('form', FormViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    #path('login/',login, name='login' ),
    #path('logout/', logout, name='logout' ),
    path('k/', k, name='k' ), 
    path('update_profile/<pk>/',updateUserView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),

    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('find/', finduserview.as_view()),

    path('update_form/<pk>/', updateFormView.as_view()),
    path('f/', formview.as_view()),
    path('forms/', forms),
    path('form/<int:pk>/delete', formdeleteview.as_view()), 
    path('count/', count),
    
    
]

handler404 = 'user.views.error404'
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



