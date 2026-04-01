from django.urls import path
from .views import SignUpView, LoginView, ForgotPasswordView, VerifyCodeView, ResetPasswordView, HealthCheckView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('health/', HealthCheckView.as_view(), name='health'),
]
