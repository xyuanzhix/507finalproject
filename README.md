# 507finalproject
# Description
This program can help you to compare the characteristics of the tracks that you are interested in. The data is from Spotify and iTunes.
# How to run
In order to use this program, you must have access to a Secret and Client ID from the Spotify API. Assuming you already have a Spotify account (free or paid), head over to https://developer.spotify.com and open your Dashboard. Click on 'Create a Client ID' and get the 'Client ID' and 'Client Secret'. Assign the 2 strings to SPOTIFY_CLIENT_ID and SPOTIFY_SECRET separately. You can find that in line 10-11 of final.py.

Now, you can run the program by running final.py simply. In the terminal, you will be asked to input the tracks' names one by one in lowercase. Then you will be asked to type the artist. Finally, you will get 4 graphs to show some characteristics of the tracks.

# Required Python Packages
requests, plotly
