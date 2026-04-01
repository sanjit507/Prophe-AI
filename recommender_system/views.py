from django.shortcuts import render
from .utils import df, recommend_properties_with_scores, get_nearby_locations, location_df

def recommend_view(request):

    locations = sorted(location_df.columns.to_list())
    apartments = sorted(df['PropertyName'].dropna().astype(str).unique().tolist())

    context = {
        'locations': locations,
        'apartments': apartments
    }

    if request.method == "POST":

        # LOCATION SEARCH
        if 'search_location' in request.POST:
            selected_location = request.POST.get('location')
            radius = request.POST.get('radius')

            if selected_location and radius:
                results = get_nearby_locations(selected_location, float(radius))
                context['location_results'] = results
                context['selected_location'] = selected_location
                context['radius'] = radius

        # RECOMMENDATION
        if 'recommend' in request.POST:
            selected_apartment = request.POST.get('apartment')

            recommendations_df = recommend_properties_with_scores(selected_apartment)

            if recommendations_df is not None:
                context['recommendations'] = recommendations_df.to_dict(orient='records')
                context['selected_apartment'] = selected_apartment

    return render(request, 'recommend.html', context)