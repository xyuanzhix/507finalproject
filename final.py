import json
import requests  
import plotly.graph_objs as go


scope = "user-library-read"

CACHE_FILENAME = "cache.json"

SPOTIFY_CLIENT_ID = 'aab31bf00a434cd8b9c81e1bd4296cad'
SPOTIFY_SECRET = '982273bd74c94b1da29111cc561312e5'


AUTH_URL = 'https://accounts.spotify.com/api/token'
# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': SPOTIFY_CLIENT_ID,
    'client_secret': SPOTIFY_SECRET,
})
# convert the response to JSON
auth_response_data = auth_response.json()
# save the access token
access_token = auth_response_data['access_token']

headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

SPOTIFY_BASE = 'https://api.spotify.com/v1/'

itunes_baseurl = "https://itunes.apple.com/search"
itunes_params = {}
itunes_params['limit'] = 50
itunes_params['media'] = 'music'


def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 



def search_track(track_name):
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params={'q': track_name, 'type': 'track', 'limit': 50})#search_id(artist_name)
    tracks = response.json()
    track_dict = {}
    track_dict[track_name] = []
    i = 0
    for track in tracks['tracks']['items']:
        track_dict[track_name].append({})
        #basic features
        track_dict[track_name][i]['artist'] = track['artists'][0]['name']
        track_dict[track_name][i]['album'] = track['album']['name']
        track_dict[track_name][i]['release_date'] = track['album']['release_date']
        track_dict[track_name][i]['id'] = track['id']
        track_dict[track_name][i]['popularity'] = track['popularity']

        #get genre from itunes
        track_dict[track_name][i]['genre'] = search_genre(track_name, track['artists'][0]['name'])

        #audio features
        response = requests.get(SPOTIFY_BASE + 'audio-features/' + track['id'], headers=headers)
        audio = response.json()
        track_dict[track_name][i]['audio_features'] = audio
        i = i + 1
    
    return track_dict

#from itunes
def search_genre(track, artist):    
    itunes_params['term'] = track
    response = requests.get(itunes_baseurl, itunes_params).json()["results"]
    for track in response:
        if track['artistName'].lower() == artist.lower():
            return track['primaryGenreName']
    return '--'
 

def cache_or_fetch(name):
    ''' 
    check if the information is in cache
    
    '''    
    cache = open_cache()
    if (name in cache.keys()):         
        print("Using cache")        
     
    else:    
        print("Fetching")        
        cache[name] = search_track(name)     
        save_cache(cache)        
    return cache[name] 


if __name__ == '__main__':

    input_track = input('Hi, which song do you want to learn about? Plz input in lowercase: ')
    track_dict = {}
    track_dict.update(cache_or_fetch(input_track))
    while True:
        input_track = input('any other tracks? If no, input "NO": ')
        if input_track == "NO":
            print("Next Step! ")
            break
        else: 
            track_dict.update(cache_or_fetch(input_track))
 
    #artist
    with_artist = {}
    print('Since many singers have released songs of the same name, who is your target singer?')
    artists = input('Input the name in lowercase and use ", " between 2 artists. Or input "NONE" to skip this step: ')
    if artists == "NONE":
        print("Next Step! ")
        with_artist = track_dict
    else:
        artists = list(artists.split(', '))        
        for track, info in track_dict.items():
            with_artist[track] = []
            for i in range(len(info)):
                for artist in artists:
                    if artist == info[i]['artist'].lower():
                        #print(type(with_artist[track]))
                        with_artist[track].append(info[i])
    
   

    search_result = {}
    for track, info in with_artist.items():
        if info != []:
            search_result[track] = with_artist[track]

    #presentation
    #build the x-axis(track+artist)
    print('list or the tracks: ')
    track_artist = []
    #y-axis
    popularity = []
    release_year = []
    energy = []
    valence = []
    danceability = []
    for track, info in search_result.items():
        for each in info:
            artist = each['artist']
            if track + '-' + artist in track_artist:
                continue
            else:
                track_artist.append(track + '-' + artist)
                print(track + '-' + artist)
                popularity.append(each['popularity'])
                release_year.append(int((each['release_date']).split('-')[0]))
                energy.append(each['audio_features']['energy'])
                valence.append(each['audio_features']['valence'])
                danceability.append(each['audio_features']['danceability'])
    while True:
        print('Which features do you want to learn about the tracks? Please choose:')
        option = input('popularity --- 1; realease time --- 2; relationship of popularity and realease time --- 3; audio --- 4; END THE QUERY --- PAK: ')
        #popularity bar
        if option == '1':
            bar_popu = go.Bar(x = track_artist, y = popularity)
            popu_layout = go.Layout(title = 'popularity')
            fig_popularity = go.Figure(data = bar_popu, layout = popu_layout)
            fig_popularity.write_html('popularity.html', auto_open = True)

        #realease year line
        elif option == '2': 
            year = go.Scatter(x = track_artist, y = release_year)
            year_layout = go.Layout(title = 'release year')
            fig_release = go.Figure(data = year, layout = year_layout)
            fig_release.write_html('release_year', auto_open = True)

        #relationship between popularity and realease year
        elif option == '3': 
            rela= go.Scatter(x = release_year, y = popularity, mode = 'markers')
            rela_layout = go.Layout(title = 'relationship between popularity and realease year')
            fig_rela = go.Figure(data = rela, layout = rela_layout)
            fig_rela.write_html('rela', auto_open = True)

        #energy-valence-danceability
        elif option == '4': 
            energy_l = go.Scatter(x = track_artist, y = energy, name = 'energy')
            valence_l = go.Scatter(x = track_artist, y = valence, name = 'valence')
            danceability_l = go.Scatter(x = track_artist, y = danceability, name = 'danceability')
            layout = go.Layout(title = 'energy-valence-danceability')
            fig_e_v_d = go.Figure(data = [energy_l, valence_l, danceability_l], layout = layout)
            fig_e_v_d.write_html('energy-valence-danceability', auto_open = True)
        else:
            print('Thank you! Bye.')
            break


    with open('result.json', 'w') as f:
        json.dump(search_result, f)
    
    