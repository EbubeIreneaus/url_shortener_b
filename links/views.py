import json
import cloudinary
from django.http import HttpResponse, JsonResponse
from .models import Link
from rest_framework.views import APIView
import random
import string
import qrcode
from django.conf import settings
import os
from io import BytesIO
from PIL import Image

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_NAME'),
    api_key = os.getenv('CLOUDINARY_KEY'),
    api_secret=os.getenv('CLOUDINARY_SECREAT')
)


img_byte = BytesIO()
# Create your views here.
def generate_key(length):
    rand_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    if Link.objects.filter(key=rand_key).exists():
        generate_key(7)
    return rand_key


class Isllinks(APIView):
    def get(self, request):
        key = request.GET.get('key', '')
        if key is not '':
            try:
                links = Link.objects.get(key=key)
                return JsonResponse({'status': 'success', 'redirect': links.link})
            except Exception as e:
                return JsonResponse({'status': 'failed', 'code': str(e)})
        return JsonResponse({'status': "failed", 'code': 'invalid url address'})

    def post(self, request):
        data = json.loads(request.body)
        link = data['link']
        if not link.startswith('http://') and not link.startswith('https://'):
            return JsonResponse({'status': "failed", 'code': 'invalid url address'})
        key = generate_key(7)
        if link:
            try:
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                                   box_size=10, border=1)
                qr.add_data(f'https://isls.netlify.app/{key}')
                qr.make(fit=True)
                img = qr.make_image(fill_color='black', back_color='white')
                img.save(img_byte, format="png")
                img_byte.seek(0)
                uploaded_img = cloudinary.uploader.upload(img_byte, folder='QRImages', resource_type='image')
                Link.objects.create(key=key, link=link, qr_src=uploaded_img['secure_url'])
                return JsonResponse({'status': 'success',
                                     'qr_src': uploaded_img['secure_url'],
                                     'shortened_link': f'https://isls.netlify.app/{key}'})
            except Exception as e:
                return JsonResponse({'status': "failed", 'code': str(e)})
        return JsonResponse({'status': "failed", 'code': 'could not detect link'})
