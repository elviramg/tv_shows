import requests
import json

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YjQ2MTU5NTE2ZDM4NTllYjRlYzMyNDlhYzNiN2VhNSIsIm5iZiI6MTcyMjU0MzEyMS4xNzA0NDcsInN1YiI6IjY2YWFjNWFkNTE4MmMwZDEzNTQ2NTgyYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.HSnc8ZCA5OWPtmUOT3ZN1m7xiojuBJmI7Ng1o65eCOU"
}
BASE_URL = "https://api.themoviedb.org/3"

def get_top_rated(BASE_URL, headers):
    all_results = []
    
    for number in range(1, 51):  
        url = f"{BASE_URL}/tv/top_rated?language=en-US&page={number}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            page_data = response.json()
            results = page_data.get('results', [])
            all_results.extend(results)
            print(f"Página {number}: Obtenidos {len(results)} shows")
        else:
            print(f"Error en la página {number}: {response.status_code}")
    
    print(f"Total de shows obtenidos: {len(all_results)}")
    return all_results

def get_genre(base_url, headers):
    url = f"{base_url}/genre/tv/list?language=en"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        genres = response.json().get('genres', [])
        return {genre['id']: genre['name'] for genre in genres}
    else:
        print(f"Error obteniendo géneros: {response.status_code}")
        return {}

def get_genre_names(genre_ids, genre_map):
    return [genre_map.get(id, "Unknown") for id in genre_ids]

def clean(tv_shows_list, genre_map):
    cleaned_data = {}
    
    for show in tv_shows_list:
        name = show.get('name')
        if not name:
            continue  
        
        genre_ids = show.get('genre_ids', [])
        genres = get_genre_names(genre_ids, genre_map)
        
        cleaned_show = {
            'genres': genres,
            'original_language': show.get('original_language', ''),
            'overview': show.get('overview', ''),
            'popularity': show.get('popularity', 0),
            'vote_average': show.get('vote_average', 0),
            'vote_count': show.get('vote_count', 0)
        }
        
        cleaned_data[name] = cleaned_show
    
    return cleaned_data

def main():
    genre_map = get_genre(BASE_URL, headers)    
    top_rated = get_top_rated(BASE_URL, headers)    
    cleaned_data = clean(top_rated, genre_map)

    for i, (name, show) in enumerate(cleaned_data.items()):
        print(f"\n{name}:")
        print(json.dumps(show, indent=2))
        if i == 4:  
            break

    print(f"\nTotal de shows procesados: {len(cleaned_data)}")

if __name__ == "__main__":
    main()