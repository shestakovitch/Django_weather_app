import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
from environs import Env


def index_page(request):
    URL = 'http://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no'

    if request.method == 'POST':
        form = CityForm(request.POST)
        obj = City.objects.filter(name=request.POST['name'])

        if form.is_valid():
            if 'add' in request.POST:
                if not obj:
                    form.save()
            elif 'del' in request.POST:
                if obj:
                    obj.delete()

    form = CityForm()

    cities = City.objects.all()
    weather_data = []

    env = Env()
    env.read_env()
    token = env('API_KEY')

    for city in cities:
        r = requests.get(URL.format(token, city)).json()
        try:
            city_weather = {
                'city': r['location']['name'],
                'temperature': r['current']['temp_c'],
                'wind': r['current']['wind_kph'],
                'description': r['current']['condition']['text'],
                'icon': r['current']['condition']['icon']
            }
            weather_data.append(city_weather)
        except:
            City.objects.filter(name=city).delete()

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'index.html', context)
