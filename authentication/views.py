import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, views
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from .models import User

class SignUpView(views.APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user:
                return Response(UserSerializer(user).data)
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(views.APIView):
    def post(self, request):
        email = request.data.get('email', '')
        if email: email = email.strip().lower()
        try:
            user = User.objects.get(email=email)
            # Generate 4-digit OTP
            otp = f"{random.randint(1000, 9999)}"
            user.reset_code = otp
            user.save()

            log_msg = f"--- [{email}] RESET CODE: {otp} ---\n"
            print(log_msg) 
            try:
                with open("logs.txt", "a") as f:
                    f.write(log_msg)
            except:
                pass

            # Prepare Email Data
            subject = 'Password Reset OTP - MRI Seq Assist'
            message = f'Your 4-digit OTP for password reset is: {otp}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            import threading
            def send_email_async(subj, msg, sender, recipients, target_email):
                print(f"DEBUG: Starting async email send to {target_email} via Mailgun...")
                try:
                    send_mail(subj, msg, sender, recipients)
                    print(f"--- SUCCESS: Email sent to {target_email} ---")
                except Exception as e:
                    print(f"--- ASYNC MAILGUN ERROR for {target_email}: {str(e)} ---")

            # Start thread with explicit arguments
            thread = threading.Thread(
                target=send_email_async, 
                args=(subject, message, from_email, recipient_list, email)
            )
            thread.daemon = True
            thread.start()

            return Response({
                "message": "4-digit OTP generated and sending...",
                "code": otp
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User with this email not found"}, status=status.HTTP_404_NOT_FOUND)

class VerifyCodeView(views.APIView):
    def post(self, request):
        email = request.data.get('email', '')
        if email: email = email.strip().lower()
        code = request.data.get('code')
        try:
            user = User.objects.get(email=email, reset_code=code)
            return Response({"message": "Code verified"})
        except User.DoesNotExist:
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(views.APIView):
    def post(self, request):
        email = request.data.get('email', '')
        if email: email = email.strip().lower()
        code = request.data.get('code')
        password = request.data.get('password') or request.data.get('new_password')
        if not password:
            return Response({"error": "Password cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email, reset_code=code)
            user.set_password(password)
            user.reset_code = None
            user.save()
            return Response({"message": "Password reset successful"})
        except User.DoesNotExist:
            return Response({"error": "Invalid session"}, status=status.HTTP_400_BAD_REQUEST)

class HealthCheckView(views.APIView):
    def get(self, request):
        return Response({"status": "healthy", "message": "MRI Seq Assist Backend is running"}, status=status.HTTP_200_OK)
