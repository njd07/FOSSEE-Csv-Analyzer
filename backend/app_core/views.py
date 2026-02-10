import io
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from .models import UploadedDataset
from .serializers import DatasetSerializer
from .utils import compute_summary, parse_csv_file
from .tasks import cleanup_old_datasets


# register new user, return token
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uname = request.data.get('username', '').strip()
        pwd = request.data.get('password', '').strip()
        email = request.data.get('email', '').strip()

        if not uname or not pwd:
            return Response({'error': 'Username and password required.'}, status=400)
        if User.objects.filter(username=uname).exists():
            return Response({'error': 'Username already taken.'}, status=400)

        user = User.objects.create_user(username=uname, password=pwd, email=email)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username}, status=201)


# upload csv and get summary
class UploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        f = request.FILES.get('file')
        if not f:
            return Response({'error': 'No file provided.'}, status=400)

        try:
            df = parse_csv_file(f)
        except Exception as e:
            return Response({'error': f'Bad CSV: {e}'}, status=400)

        summary = compute_summary(df)
        f.seek(0)
        ds = UploadedDataset.objects.create(
            name=f.name, csv_file=f,
            summary=summary, row_count=len(df)
        )
        cleanup_old_datasets()
        return Response(DatasetSerializer(ds).data, status=201)


# last 5 uploads
class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ds = UploadedDataset.objects.all()[:5]
        return Response(DatasetSerializer(ds, many=True).data)


# summary for one dataset
class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        did = request.query_params.get('id')
        if not did:
            return Response({'error': 'Missing id.'}, status=400)
        try:
            ds = UploadedDataset.objects.get(id=did)
        except UploadedDataset.DoesNotExist:
            return Response({'error': 'Not found.'}, status=404)
        return Response(ds.summary)


# chart-ready data + rows
class ChartDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        did = request.query_params.get('id')
        if not did:
            return Response({'error': 'Missing id.'}, status=400)
        try:
            ds = UploadedDataset.objects.get(id=did)
        except UploadedDataset.DoesNotExist:
            return Response({'error': 'Not found.'}, status=404)

        dist = ds.summary.get('type_distribution', {})
        avgs = ds.summary.get('averages', {})

        # read rows for table
        rows = []
        try:
            df = parse_csv_file(ds.csv_file)
            rows = df.to_dict(orient='records')
        except Exception:
            pass

        return Response({
            'labels': list(dist.keys()),
            'counts': list(dist.values()),
            'averages': avgs,
            'rows': rows,
        })


# generate pdf report
class ReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        did = request.query_params.get('id')
        if not did:
            return Response({'error': 'Missing id.'}, status=400)
        try:
            ds = UploadedDataset.objects.get(id=did)
        except UploadedDataset.DoesNotExist:
            return Response({'error': 'Not found.'}, status=404)

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4)
        styles = getSampleStyleSheet()
        els = []

        # title and info
        els.append(Paragraph("Equipment Data Report", styles['Title']))
        els.append(Spacer(1, 0.3 * inch))
        els.append(Paragraph(f"File: {ds.name}", styles['Normal']))
        els.append(Paragraph(f"Uploaded: {ds.uploaded_at:%Y-%m-%d %H:%M}", styles['Normal']))
        els.append(Paragraph(f"Rows: {ds.row_count}", styles['Normal']))
        els.append(Spacer(1, 0.3 * inch))

        tbl_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b6cb4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ])

        # averages table
        avgs = ds.summary.get('averages', {})
        if avgs:
            els.append(Paragraph("Parameter Averages", styles['Heading2']))
            data = [['Parameter', 'Average']] + [[k, str(v)] for k, v in avgs.items()]
            t = Table(data, colWidths=[2.5 * inch, 2 * inch])
            t.setStyle(tbl_style)
            els.append(t)
            els.append(Spacer(1, 0.3 * inch))

        # type distribution table
        dist = ds.summary.get('type_distribution', {})
        if dist:
            els.append(Paragraph("Type Distribution", styles['Heading2']))
            data = [['Type', 'Count']] + [[k, str(v)] for k, v in dist.items()]
            t = Table(data, colWidths=[2.5 * inch, 2 * inch])
            t.setStyle(tbl_style)
            els.append(t)

        doc.build(els)
        buf.seek(0)
        resp = HttpResponse(buf, content_type='application/pdf')
        resp['Content-Disposition'] = f'attachment; filename="report_{ds.id}.pdf"'
        return resp
