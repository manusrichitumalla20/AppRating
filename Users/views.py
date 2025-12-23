from django.shortcuts import render , redirect
from django.contrib import messages
from Users.models import UserRegisterModel
from django.conf import settings
from Users.forms import UserRegisterForm
import re
import sys
import time
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
import os
from sklearn.model_selection import train_test_split

def base(request):
    return render(request , 'base.html')

def UserRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request , 'Registered successfully')
            return redirect('Userlogin')
        else:
            messages.warning(request , 'Invalid credentials')
    else:
        form = UserRegisterForm()
    return render(request , 'Userregister.html' , {'form':form})


def Userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            if username and password:
                user = UserRegisterModel.objects.get(Username=username , Password=password)
                if user.status == 'Activate':
                    request.session['user_id'] = user.id
                    request.session['username'] =username
                    request.session['Email'] =user.Email
                    request.session['Phone_No'] =user.Phone_No
                    return redirect('UserHome')
                else:
                    messages.warning(request , 'User is deactivated')
                    return redirect('Userlogin')
            else:
                messages.warning(request , 'Invalid credentials')
                return redirect('Userlogin')

        except Exception as e:
            messages.warning(request , f'{e}')

            
    return render(request , 'Userlogin.html')


def UserHome(request):
    user = request.session.get('username')
    email = request.session.get('Email')
    phone = request.session.get('Phone_No')
    return render(request , 'users/UserHome.html' , {'user':user , 'email':email , 'phone':phone})

#=========================TRAINING========================================
def training(request):
    user = request.session.get('username')
    data = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'googleplaystore.csv'))
    from sklearn.preprocessing import LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error , mean_squared_error , r2_score
    le=LabelEncoder()
    data['App'] = le.fit_transform(data['App'])
    data['Category'] = le.fit_transform(data['Category'])
    data['Rating'] = le.fit_transform(data['Rating'])
    data['Reviews'] = le.fit_transform(data['Reviews'])
    data['Installs'] = le.fit_transform(data['Installs'])
    data['Type'] = le.fit_transform(data['Type'])
    data['Price'] = le.fit_transform(data['Price'])
    data['Content Rating'] = le.fit_transform(data['Content Rating'])
    data['Genres'] = le.fit_transform(data['Genres'])
    data['Last Updated'] = le.fit_transform(data['Last Updated'])
    data['Current Ver'] = le.fit_transform(data['Current Ver'])
    feature = ['App', 'Category' , 'Reviews' ,  'Installs' , 'Genres']
    x=data[feature]
    y = data['Rating']  
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier()
    x_train , x_test , y_train , y_test = train_test_split(x, y , random_state=42)
    model.fit(x_train,y_train) 
    y_pre = model.predict(x_test)
    mae = mean_absolute_error(y_test , y_pre)
    mse = mean_squared_error(y_test , y_pre)
    r2 = r2_score(y_test , y_pre)

    return render(request , 'users/training.html', {'mae':mae , 'mse':mse ,  "user": user})


def DatasetView(request):
    user = request.session.get('username')
    data = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'googleplaystore.csv'))
    from sklearn.preprocessing import LabelEncoder
    le=LabelEncoder()
    data['App'] = le.fit_transform(data['App'])
    data['Category'] = le.fit_transform(data['Category'])
    data['Rating'] = le.fit_transform(data['Rating'])
    data['Reviews'] = le.fit_transform(data['Reviews'])
    data['Installs'] = le.fit_transform(data['Installs'])
    data['Type'] = le.fit_transform(data['Type'])
    data['Price'] = le.fit_transform(data['Price'])
    data['Content Rating'] = le.fit_transform(data['Content Rating'])
    data['Genres'] = le.fit_transform(data['Genres'])
    data['Last Updated'] = le.fit_transform(data['Last Updated'])
    data['Current Ver'] = le.fit_transform(data['Current Ver'])
    data = data.head(100)


    return render(request , 'users/datasetview.html' , {'data':data.to_html , "user": user})

#=======================================PREDICATION=======================================


import os
import re
import time
import datetime
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

def Predication(request):
    user = request.session.get('username')
    if request.method == 'POST':
        app = int(request.POST.get('app'))
        category = int(request.POST.get('category'))
        reviews = int(request.POST.get('reviews'))
        installs = int(request.POST.get('installs'))
        genres = int(request.POST.get('genres'))
        
        # Path to the CSV file
        data_path = os.path.join(settings.MEDIA_ROOT, 'googleplaystore.csv')
        
        # Read the CSV file into a DataFrame
        data = pd.read_csv(data_path)
        
        # Encode categorical features
        le = LabelEncoder()
        data['App'] = le.fit_transform(data['App'])
        data['Category'] = le.fit_transform(data['Category'])
        data['Rating'] = le.fit_transform(data['Rating'])
        data['Reviews'] = le.fit_transform(data['Reviews'])
        data['Installs'] = le.fit_transform(data['Installs'])
        data['Type'] = le.fit_transform(data['Type'])
        data['Price'] = le.fit_transform(data['Price'])
        data['Content Rating'] = le.fit_transform(data['Content Rating'])
        data['Genres'] = le.fit_transform(data['Genres'])
        data['Last Updated'] = le.fit_transform(data['Last Updated'])
        data['Current Ver'] = le.fit_transform(data['Current Ver'])
        
        # Features and target
        feature = ['App', 'Category', 'Reviews', 'Installs', 'Genres']
        x = data[feature]
        y = data['Rating']
        
        # Train-test split
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42)
        
        # Model training
        model = RandomForestRegressor()
        model.fit(x_train, y_train)
        
        # Prediction
        pre = model.predict([[app, category, reviews, installs, genres]])
        print(pre)
        
        return render(request, 'users/predication.html', {"user": user, "prediction": pre[0]})
    
    return render(request, 'users/predication.html', {"user": user})
