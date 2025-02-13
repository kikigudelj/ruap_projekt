import os
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import House
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from .forms import HouseRentalForm,HouseRentForm
import plotly.express as px
import pandas as pd

def home(request):
    context = {}
    return render(request,'home.html',context)

def house_rentals(request):
    houses = House.objects.all()  

    house_data = pd.DataFrame(list(houses.values('square_meters', 'price_per_month', 'num_rooms', 'year_built')))

    scatter_fig = px.scatter(house_data, x='square_meters', y='price_per_month', 
                             title='Price Distribution Based on Area',
                             labels={'square_meters': 'Area (m²)', 'price_per_month': 'Price per Month (Euro)'})
    scatter_html = scatter_fig.to_html(full_html=False)

    histogram_fig = px.histogram(
    house_data, 
    x='price_per_month', 
    nbins=20, 
    title='Price Distribution of Rentals',
    color_discrete_sequence=['#3498db'], 
    marginal='rug', 
    opacity=0.75
)

    histogram_fig.update_layout(
        xaxis_title='Price per Month (Euro)',
        yaxis_title='Number of Houses',
        bargap=0.05, 
        template='plotly_white'  
    )

    histogram_html = histogram_fig.to_html(full_html=False)

    if not house_data.empty:
        line_fig = px.line(house_data.groupby('year_built').mean().reset_index(), 
                           x='year_built', y='price_per_month', 
                           title='Impact of Year Built on Price',
                           labels={'year_built': 'Year Built', 'price_per_month': 'Average Price (Euro)'})
        line_html = line_fig.to_html(full_html=False)
    else:
        line_html = None  

    if not house_data.empty and 'num_rooms' in house_data:
        house_data = house_data.dropna(subset=['num_rooms']) 
        house_data['num_rooms'] = house_data['num_rooms'].astype(str)  

        pie_fig = px.pie(house_data, names='num_rooms', title='Share of Houses by Number of Rooms', hole=0.3)
        pie_html = pie_fig.to_html(full_html=False)
    else:
        pie_html = None

    correlation_matrix = house_data[['square_meters', 'price_per_month', 'num_rooms']].corr()
    heatmap_fig = px.imshow(correlation_matrix, text_auto=True, 
                            title='The correlation between variables (Square Meters, Price, Number of Rooms)')
    heatmap_html = heatmap_fig.to_html(full_html=False)

    # Form Handling
    if request.method == 'POST':
        form = HouseRentalForm(request.POST, request.FILES)
        if form.is_valid():
            house = form.save(commit=False)
            house.owner = request.user  
            house.save()
            return redirect('house_rentals')
    else:
        form = HouseRentalForm()

    return render(request, 'house_rentals.html', {
        'form': form, 
        'houses': houses,
        'scatter_html': scatter_html,
        'histogram_html': histogram_html,
        'line_html': line_html,
        'pie_html': pie_html,
        'heatmap_html': heatmap_html,
    })


def house_detail(request, house_id):
    house = get_object_or_404(House, id=house_id)
    context = {
        'house': house,
    }
    return render(request,'house_detail.html', context)


def house_detail(request, house_id):
    house = get_object_or_404(House, id=house_id)
    context = {
        'house': house,
    }
    return render(request,'house_detail.html',context)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
        else:
            return render(request, "login.html", {"form": form, "error": "Neispravni podaci!"})
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Uspješno ste se registrirali!")
            return redirect('login')  
        else:
            return render(request, "register.html", {"form": form, "error": "Pogreška u registraciji!"})
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('home')

def rent_your_house(request):
    if request.method == 'POST':
        form = HouseRentalForm(request.POST, request.FILES)
        if form.is_valid():
            house = form.save(commit=False)
            house.owner = request.user  
            house.save()
            return redirect('rent_your_house') 
    else:
        form = HouseRentalForm()

    return render(request, 'rent_house.html', {'form': form})



####### AZURE MODEL ############
##################################
############################

from django.shortcuts import render
import urllib.request
import json
import ssl
import os

def allowSelfSignedHttps(allowed):

    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def rent_house_predict(request):
    allowSelfSignedHttps(True)  
    
    if request.method == 'POST':
        form = HouseRentForm(request.POST)
        if form.is_valid():
            # Podaci za slanje prema API-u
            data = {
                "Inputs": {
                    "input1": [
                        {
                            "area": form.cleaned_data['area'],
                            "room_num": form.cleaned_data['room_num'],
                            "floor": form.cleaned_data['floor'],
                            "total_floor": form.cleaned_data['total_floor'],
                            "year_built": form.cleaned_data['year_built'],
                            "balcony": form.cleaned_data['balcony'],
                            "basement": form.cleaned_data['basement'],
                            "dish_washer": form.cleaned_data['dish_washer'],
                            "fridge": form.cleaned_data['fridge'],
                            "furniture": form.cleaned_data['furniture'],
                            "tv_set": form.cleaned_data['tv_set'],
                            "air_conditioning": form.cleaned_data['air_conditioning'],
                            "elevator": form.cleaned_data['elevator'],
                            "garage_parking": form.cleaned_data['garage_parking'],
                            "secure_doors_windows": form.cleaned_data['secure_doors_windows'],
                            "monitoring_security": form.cleaned_data['monitoring_security'],
                            "internet": form.cleaned_data['internet'],
                            "gross_price": 1000
                        }
                    ]
                },
                "GlobalParameters": {
                    "method": "predict"
                }
            }

            body = str.encode(json.dumps(data))
            url = 'http://29aeee43-ab2e-4027-99ee-601723ace47f.westeurope.azurecontainer.io/score'
            api_key = '88echvQKEkOePwsiWUuuzHgdUE5QreoQ'  

            headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
            req = urllib.request.Request(url, body, headers)

            try:
                response = urllib.request.urlopen(req)
                result = response.read()
                result_json = json.loads(result)

                scored_label = result_json["Results"]["WebServiceOutput0"][0]["Scored Labels"]/4.5
                standard_deviation = 0.5
                confidence_interval = (scored_label - 1.96 * standard_deviation, scored_label + 1.96 * standard_deviation)
                print("API Response:", result_json) 
                return render(request, 'result.html', {
                    'scored_label': scored_label,
                    'confidence_interval': confidence_interval,
                    'form': form
                })

            except urllib.error.HTTPError as error:
                print("The request failed with status code: " + str(error.code))
                print(error.info())
                print(error.read().decode("utf8", 'ignore'))
                return render(request, 'error.html', {'error': 'API Error'})
        else:
            return render(request, 'prediction.html', {'form': form, 'error': 'Invalid data'})
    else:
        form = HouseRentForm()
        return render(request, 'prediction.html', {'form': form})

def calculate_confidence_interval(scored_label):
    error_margin = 0.05 * scored_label  
    lower_bound = scored_label - error_margin
    upper_bound = scored_label + error_margin
    return lower_bound, upper_bound




#####################GRAFOVI

