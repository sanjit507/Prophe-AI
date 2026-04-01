
import json
from pathlib import Path

import pandas as pd
import plotly
import plotly.express as px

from django.shortcuts import render
from django.conf import settings

def analytics_map(request):
    data_path = Path(settings.BASE_DIR) / 'Analytics' / 'data' / 'data_viz1.csv'
    new_df = pd.read_csv(data_path)

    # Filtering options
    sectors = sorted(new_df['sector'].dropna().unique().tolist())
    pie_metrics = ['bedRoom', 'property_type', 'society']
    
    selected_sector = request.GET.get('sector', 'overall')
    selected_metric = request.GET.get('metric', 'bedRoom')

    # Data for Map (always needs sectors even if filtered)
    if selected_sector != 'overall' and selected_sector in sectors:
        map_df = new_df[new_df['sector'] == selected_sector]
        plot_df = map_df
    else:
        map_df = new_df
        plot_df = new_df

    cols = ['price','price_per_sqft','built_up_area','latitude','longitude']
    group_df = map_df.groupby('sector')[cols].mean().reset_index()
    group_df = group_df.dropna(subset=["latitude","longitude"])

    # Create Map
    fig = px.scatter_mapbox(  
        group_df,
        lat="latitude",
        lon="longitude",
        color="price_per_sqft",
        size='built_up_area',
        zoom=10 if selected_sector == 'overall' else 13,
        mapbox_style="carto-positron",
        hover_name="sector",
        height=700
    )

    # Create Scatter (Area vs Price)
    fig1 = px.scatter(
        plot_df,
        x="built_up_area",
        y="price",
        color="bedRoom",
        title=f"Area vs Price ({selected_sector})"
    )

    # Create Pie Chart with Dynamic Metric
    fig2 = px.pie(
        plot_df,
        names=selected_metric if selected_metric in pie_metrics else 'bedRoom',
        title=f"{selected_metric.replace('_', ' ').title()} Distribution ({selected_sector})"
    )

    # Create Box Plot (BHK Price Range) - Filters for <= 4 bedrooms as requested
    box_df = plot_df[plot_df['bedRoom'] <= 4]
    fig3 = px.box(
        box_df,
        x='bedRoom',
        y='price',
        title=f'BHK Price Range ({selected_sector})'
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    return render(request, 'map.html', {
        'graphJSON': graphJSON, 
        'graphJSON1': graphJSON1,
        'graphJSON2': graphJSON2,
        'graphJSON3': graphJSON3,
        'sectors': sectors,
        'selected_sector': selected_sector,
        'pie_metrics': pie_metrics,
        'selected_metric': selected_metric
    })