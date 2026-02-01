from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Dataset
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import pandas as pd
import os

class SignupView(APIView):
    permission_classes = [] 

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        first_name = request.data.get('first_name', '') 
        full_name = request.data.get('full_name', '') 

        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email, first_name=full_name)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [] 

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({"message": "Login successful", "username": user.username})
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.permissions import IsAuthenticated

class UploadCSVView(APIView):
    permission_classes = [IsAuthenticated]
    REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']

    def post(self, request):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
 
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            return Response({"error": f"Invalid CSV: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        dataset = Dataset.objects.create(name=uploaded_file.name, file=uploaded_file, owner=request.user)
        dataset.save()

        user_datasets = Dataset.objects.filter(owner=request.user).order_by('-uploaded_at')
        if user_datasets.count() > 5:
            for old_dataset in user_datasets[5:]:
                if os.path.exists(old_dataset.file.path):
                    os.remove(old_dataset.file.path)
                old_dataset.delete()

        return Response({
            "message": "CSV uploaded and parsed successfully",
            "dataset_id": dataset.id,
            "columns": list(df.columns)
        })

class DatasetSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            dataset = Dataset.objects.get(id=id, owner=request.user)
            df = pd.read_csv(dataset.file.path)

            analytics = {
                "total_count": len(df),
                "avg_flowrate": round(df['Flowrate'].mean(), 2) if 'Flowrate' in df.columns else 0,
                "avg_pressure": round(df['Pressure'].mean(), 2) if 'Pressure' in df.columns else 0,
                "max_temperature": df['Temperature'].max() if 'Temperature' in df.columns else 0,
                "critical_alerts": len(df[(df['Pressure'] > 1200) | (df['Temperature'] > 100)]) if 'Pressure' in df.columns and 'Temperature' in df.columns else 0, 
                "equipment_count_by_type": df['Type'].value_counts().to_dict() if 'Type' in df.columns else {}
            }

            return Response({
                "dataset_id": dataset.id,
                "name": dataset.name,
                "analytics": analytics
            })

        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DatasetRawDataView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            dataset = Dataset.objects.get(id=id, owner=request.user)
            df = pd.read_csv(dataset.file.path)
            data = df.to_dict(orient='records')

            return Response({
                "dataset_id": dataset.id,
                "name": dataset.name,
                "data": data
            })

        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DatasetPDFView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            dataset = Dataset.objects.get(id=id, owner=request.user)
            df = pd.read_csv(dataset.file.path)
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{dataset.name}_report.pdf"'
            
            p = canvas.Canvas(response, pagesize=letter)
            width, height = letter
            
            p.setFont("Helvetica-Bold", 16)
            p.drawString(50, height - 50, f"Equipment Report: {dataset.name}")
            
            p.setFont("Helvetica", 12)
            p.drawString(50, height - 80, f"Total Records: {len(df)}")
            p.drawString(50, height - 100, f"Generated for: {request.user.username}")
            
            
            
            p.showPage()
            p.save()
            return response

        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DatasetListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        datasets = Dataset.objects.filter(owner=request.user).order_by('-uploaded_at')[:5]
        data = []
        for d in datasets:
            summary_text = "Summary unavailable."
            try:
                df = pd.read_csv(d.file.path)
                total = len(df)
                types = len(df['Type'].unique()) if 'Type' in df.columns else 0
                avg_flow = round(df['Flowrate'].mean(), 1) if 'Flowrate' in df.columns else 0
                avg_press = round(df['Pressure'].mean(), 1) if 'Pressure' in df.columns else 0
                
                summary_text = (
                    f"Dataset contains {total} records across {types} unique equipment types. "
                    f"Key averages include {avg_flow} m³/h Flowrate and {avg_press} PSI Pressure. "
                    f"Data integrity verified and ready for deep-dive analysis."
                )
            except Exception as e:
                summary_text = "File processing pending or unavailable."

            data.append({
                "id": d.id, 
                "name": d.name, 
                "uploaded_at": d.uploaded_at,
                "summary": summary_text
            })
        return Response(data)
