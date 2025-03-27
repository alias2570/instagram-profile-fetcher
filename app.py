from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_instagram_profile_picture(username):
    url = f'https://www.instagram.com/{username}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # تلاش برای یافتن تگ <meta> که شامل لینک تصویر پروفایل است
        image_tag = soup.find('meta', property='og:image')
        if image_tag:
            return image_tag['content']  # برمی‌گرداند URL تصویر پروفایل
        else:
            return None  # اگر تصویر پروفایل یافت نشود
    else:
        return None  # در صورت بروز خطا در درخواست HTTP

@app.route('/getProfilePicture')
def get_profile_picture():
    username = request.args.get('username')
    if username:
        profile_picture_url = get_instagram_profile_picture(username)
        if profile_picture_url:
            return jsonify({'profile_picture': profile_picture_url})
        else:
            return jsonify({'profile_picture': 'No image found or private profile_
