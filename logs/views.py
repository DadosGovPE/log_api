from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import os
from django.http import FileResponse

class SetFolderView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        folder = request.data.get('folder', None)
        if folder and os.path.isdir(folder):
            settings.LOG_FOLDER = folder
            return Response({"message": "Folder set successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid folder path"}, status=status.HTTP_400_BAD_REQUEST)

class DownloadLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        folder = getattr(settings, 'LOG_FOLDER', None)
        if folder:
            log_file_path = os.path.join(folder, 'access.log.1')
            print(log_file_path)
            if os.path.isfile(log_file_path):
                response = FileResponse(open(log_file_path, 'rb'))
                return response
            else:
                return Response({"error": "Log file not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Log folder not set"}, status=status.HTTP_400_BAD_REQUEST)
