from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, LoginSerializer, TokenSerializer
from utils.permissions import IsSuperAdmin, IsAdmin


class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Redirect to appropriate dashboard if already logged in
        if request.user.is_authenticated:
            if request.user.is_superadmin or request.user.is_admin:
                return redirect('/tasks/panel_dashboard/')
            return redirect('/tasks/')
        return render(request, 'users/login.html')
    
    @csrf_exempt
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            
            # Create JWT tokens
            refresh = RefreshToken.for_user(user)
            
            # Store tokens in session for web access
            request.session['access_token'] = str(refresh.access_token)
            request.session['refresh_token'] = str(refresh)
            
            # Return JSON response for API
            if request.content_type == 'application/json':
                data = {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserSerializer(user).data
                }
                return Response(data, status=status.HTTP_200_OK)
            
            # Redirect to appropriate dashboard
            if user.is_superadmin or user.is_admin:
                return redirect('/tasks/dashboard/')
            return redirect('/tasks/')
        
        if request.content_type == 'application/json':
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return render(request, 'users/login.html', {'error': 'Invalid credentials'})


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('/users/login/')
    
    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsSuperAdmin()]
        return [IsAdmin()]
    
    def perform_create(self, serializer):
        user = serializer.save()
        if self.request.user.is_superadmin:
            # SuperAdmin can set any role
            pass
        elif self.request.user.is_admin:
            # Admin can only create regular users
            user.role = 'USER'
            user.admin = self.request.user
            user.save()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsSuperAdmin()]
        return [IsAdmin()]


class AdminUserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]
    
    def get_queryset(self):
        return User.objects.filter(role__in=['ADMIN', 'SUPERADMIN'])



# Template views for web interface
def login_view(request):
    view = CustomLoginView()
    return view.get(request)

def logout_view(request):
    view = LogoutView()
    return view.get(request)