import json
import os.path
import random
import string

import qrcode.constants
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from qrcode import QRCode
from PIL import  Image
from django.conf import  settings
# Create your views here.

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
			img_path = os.path.join(settings.MEDIA_ROOT, f'{key}.png')
			img.save(img_path)
			return JsonResponse({
				'status': 'success',
				'qr_src':f'http://127.0.0.1:8000/qr_codes/{key}.png'})
		except:

			return JsonResponse({'status': 'failed'})