import requests

def weather(request):
    response = requests.get(
        'https://api.weatherapi.com/v1/current.json?q=fergana&key=079c9a7ffa4644b1b24131018253006'
    )
    data = response.json()

    icon = data.get('current', {}).get('condition', {}).get('icon')
    temp = data.get('current', {}).get('temp_c')
    city = data.get('location', {}).get('name')
    date = data.get('location', {}).get('localtime')

    context = {
        'city': city,
        'date': date,
        'icon': icon,
        'temp': temp,
    }
    return context
