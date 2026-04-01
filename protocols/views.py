import logging
logger = logging.getLogger(__name__)

from rest_framework import viewsets, views, status
from rest_framework.response import Response
from .models import Region, Indication, SavedProtocol, ProtocolRequest
from .serializers import RegionSerializer, IndicationSerializer, ProtocolSerializer, ProtocolRequestSerializer

class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class IndicationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IndicationSerializer

    def get_queryset(self):
        region_name = self.request.query_params.get('region')
        if region_name:
            return Indication.objects.filter(region__name=region_name)
        return Indication.objects.all()

class SaveProtocolView(views.APIView):
    def post(self, request):
        try:
            print(f"DEBUG: SaveProtocolView ENTRY. Data: {request.data}")
            data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
            
            # Simplified user handling: let serializer handle it or set to None if empty
            if 'user' in data and (data['user'] == "" or data['user'] == "null" or data['user'] is None):
                data['user'] = None

            serializer = ProtocolSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            print(f"DEBUG: SaveProtocol errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"ERROR in SaveProtocolView: {str(e)}")
            return Response({"error": "Internal Server Error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MyProtocolsView(views.APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            try:
                protocols = SavedProtocol.objects.filter(user_id=int(user_id)).order_by('-created_at')
                return Response(ProtocolSerializer(protocols, many=True).data)
            except (ValueError, TypeError):
                return Response({"error": "invalid user_id"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "user_id required"}, status=status.HTTP_400_BAD_REQUEST)

class ProtocolRequestView(views.APIView):
    def post(self, request):
        try:
            print(f"DEBUG: ProtocolRequestView ENTRY. Data: {request.data}")
            data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
            
            # Simplified user handling
            if 'user' in data and (data['user'] == "" or data['user'] == "null" or data['user'] is None):
                data['user'] = None

            serializer = ProtocolRequestSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            print(f"DEBUG: ProtocolRequest errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"ERROR in ProtocolRequestView: {str(e)}")
            return Response({"error": "Internal Server Error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        user_id = request.query_params.get('user_id')
        try:
            if user_id:
                requests = ProtocolRequest.objects.filter(user_id=int(user_id)).order_by('-created_at')
            else:
                requests = ProtocolRequest.objects.all().order_by('-created_at')
            return Response(ProtocolRequestSerializer(requests, many=True).data)
        except (ValueError, TypeError, Exception) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
