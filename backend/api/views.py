from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Dataset
import pandas as pd
import os

class UploadCSVView(APIView):
    REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']

    def post(self, request):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

       
        try:
            df = pd.read_csv(file)
        except Exception as e:
            return Response({"error": f"Invalid CSV: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            return Response({"error": f"CSV must contain columns: {self.REQUIRED_COLUMNS}"}, status=status.HTTP_400_BAD_REQUEST)

       
        dataset = Dataset.objects.create(name=file.name, file=file)
        dataset.save()

       
        all_datasets = Dataset.objects.order_by('-uploaded_at')
        if all_datasets.count() > 5:
            for old_dataset in all_datasets[5:]:
                if os.path.exists(old_dataset.file.path):
                    os.remove(old_dataset.file.path)
                old_dataset.delete()

        return Response({
            "message": "CSV uploaded and parsed successfully",
            "dataset_id": dataset.id,
            "columns": list(df.columns)
        })



class DatasetSummaryView(APIView):
    def get(self, request, id):
        try:
            dataset = Dataset.objects.get(id=id)
            df = pd.read_csv(dataset.file.path)

            analytics = {
                "avg_flowrate": round(df['Flowrate'].mean(), 2),
                "max_temperature": df['Temperature'].max(),
                "min_pressure": df['Pressure'].min(),
                "equipment_count_by_type": df['Type'].value_counts().to_dict()
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
    def get(self, request, id):
        try:
            dataset = Dataset.objects.get(id=id)
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
