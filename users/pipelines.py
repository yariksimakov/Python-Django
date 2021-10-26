from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from users.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', '/method/users.get', None, urlencode(
        OrderedDict(fields=','.join(('bdate', 'sex', 'about')), access_token=response['access_token'], v=5.131)),
                          None))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    if data['sex'] == 1:
        user.userprofile.gender = UserProfile.FEMALE
    elif data['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE
    else:
        pass

    if data['about']:
        user.userprofile.about = data['about']

    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    age = timezone.now().date().year - bdate.year

    if response['user_photo']:
        photo_response = response['user_photo']
        photo_request = requests.get(photo_response)
        path_photo_pk = f'users_image/{user.pk}.jpg'
        with open(f'media/{path_photo_pk}', 'wb') as user_photo:
            user_photo.write(photo_request.content)
        user.image = path_photo_pk



    user.age = age
    if age < 18:
        user.delete()
        return AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.save()