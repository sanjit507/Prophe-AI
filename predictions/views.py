import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render

APP_DIR = Path(__file__).resolve().parent

try:
    with open('predictions/model/pipeline.pkl', 'rb') as f:
        pipeline = pickle.load(f)
    with open('predictions/model/df.pkl', 'rb') as f:
        df = pickle.load(f)
except Exception as error:
    pipeline = None
    df = None
    print('model/data load error:', error)



def _predict_form_context():
    if df is None:
        return {
            'sectors': [],
            'bedrooms': [],
            'bathrooms': [],
            'balconies': [],
            'ages': [],
            'furnishing': [],
            'luxury': [],
            'floor': [],
        }

    return {
        'sectors': sorted(df['sector'].unique().tolist()),
        'bedrooms': sorted(df['bedRoom'].unique().tolist()),
        'bathrooms': sorted(df['bathroom'].unique().tolist()),
        'balconies': sorted(df['balcony'].unique().tolist()),
        'ages': sorted(df['agePossession'].unique().tolist()),
        'furnishing': sorted(df['furnishing_type'].unique().tolist()),
        'luxury': sorted(df['luxury_category'].unique().tolist()),
        'floor': sorted(df['floor_category'].unique().tolist()),
    }


def predict(request):
    if request.method != 'POST':
        context = _predict_form_context()
        if pipeline is None or df is None:
            context['error'] = 'Model/data not loaded. Please check server logs and installed packages.'
        return render(request, 'prediction.html', context)

    if pipeline is None or df is None:
        context = _predict_form_context()
        context['error'] = 'Model/data not loaded. Please check server logs and installed packages.'
        return render(request, 'prediction.html', context)

    try:
        data = [
            request.POST['property_type'],
            request.POST['sector'],
            float(request.POST['bedroom']),
            float(request.POST['bathroom']),
            request.POST['balcony'],
            request.POST['property_age'],
            float(request.POST['area']),
            float(request.POST['servant_room']),
            float(request.POST['store_room']),
            request.POST['furnishing'],
            request.POST['luxury'],
            request.POST['floor'],
        ]

        columns = [
            'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
            'agePossession', 'built_up_area', 'servant room', 'store room',
            'furnishing_type', 'luxury_category', 'floor_category',
        ]

        df_input = pd.DataFrame([data], columns=columns)
        base_price = np.expm1(pipeline.predict(df_input))[0]
        low = round(base_price - 0.22, 2)
        high = round(base_price + 0.22, 2)

        return render(request, 'result.html', {'low': low, 'high': high})
    except Exception as error:
        context = _predict_form_context()
        context['error'] = f'Prediction error: {error}'
        return render(request, 'prediction.html', context)