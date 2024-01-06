import json
import os.path
import random
import string
import os
import qrcode.constants
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from qrcode import QRCode
from PIL import  Image
from django.conf import  settings
import cloudinary
from io import BytesIO
# Create your views here.

img_bytes = BytesIO()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_NAME'),
    api_key = os.getenv('CLOUDINARY_KEY'),
    api_secret=os.getenv('CLOUDINARY_SECREAT')
)


def generate_key(length):
	rand_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

	return rand_key
class generate(APIView):
	def post(self, request):
		data = json.loads(request.body)
		text = data['txt_data']
		fcolor = data['fg_color']
		bcolor = data['bg_color']
		size = data['border_size']
		key = generate_key(7)
		try:
			qr = QRCode(
				version=1,
				error_correction=qrcode.constants.ERROR_CORRECT_L,
				box_size=10, border=size
				)
			qr.add_data(text)
			qr.make(fit=True)
			img = qr.make_image(fill_color=fcolor, back_color = bcolor)
			img.save(img_bytes, format='PNG')
			img_bytes.seek(0)
			uploaded_img = cloudinary.uploader.upload(img_bytes, folder='QRImages', resource_type='image')
			return JsonResponse({
				'status': 'success',
				'qr_src':uploaded_img['secure_url']})
		except Exception as e:
			return JsonResponse({'status': 'failed', "code":str(e)})