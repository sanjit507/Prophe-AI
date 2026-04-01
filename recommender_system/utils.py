from pathlib import Path
import pickle

import pandas as pd
from django.conf import settings

# Load datasets once (important for performance)
BASE_DIR = Path(settings.BASE_DIR)
MODEL_DIR = BASE_DIR / 'recommender_system' / 'Model'

location_df = pickle.load(open(MODEL_DIR / 'location_distance.pkl', 'rb'))
cosine_sim = pickle.load(open(MODEL_DIR / 'cosine_sim.pkl', 'rb'))
cosine_sim2 = pickle.load(open(MODEL_DIR / 'cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open(MODEL_DIR / 'cosine_sim3.pkl', 'rb'))

# Load your main dataframe (IMPORTANT: you forgot in Streamlit)
df = pd.read_csv(MODEL_DIR / 'appartments.csv')


def recommend_properties_with_scores(property_name, top_n=5):

    cosine_sim_matrix = 0.5*cosine_sim + 0.8*cosine_sim2 + 1*cosine_sim3

    matching_rows = df.index[df['PropertyName'] == property_name].tolist()

    if not matching_rows:
        return None

    property_idx = matching_rows[0]

    sim_scores = list(enumerate(cosine_sim_matrix[property_idx]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n+1]]

    top_properties = df['PropertyName'].iloc[top_indices].tolist()

    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df


def get_nearby_locations(selected_location, radius):
    result = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()

    return [
        (str(df.iloc[int(idx)]['PropertyName']), round(val / 1000, 2))
        for idx, val in result.items()
    ]