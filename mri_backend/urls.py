from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def proxy_to_fastapi(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            fastapi_url = "http://127.0.0.1:8001/ai/mri-question"
            resp = requests.post(fastapi_url, json=body, timeout=15)
            # Pass the FastAPI JSON response directly back to the app
            try:
                return JsonResponse(resp.json(), status=resp.status_code)
            except ValueError:
                return JsonResponse({'error': 'FastAPI sent invalid JSON'}, status=500)
        except Exception as e:
            return JsonResponse({'error': 'Failed to connect to FastAPI brain: ' + str(e)}, status=500)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/protocols/', include('protocols.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
    path('index.html', TemplateView.as_view(template_name='index.html')),
    path('auth.html', TemplateView.as_view(template_name='auth.html')),
    path('ai/mri-question/', proxy_to_fastapi),
]

if settings.DEBUG:
    # This allows Django to seamlessly serve css/style.css, js/app.js, and data/ files directly from mri-website
    urlpatterns += static('/', document_root=settings.STATICFILES_DIRS[0])
