import folium

def marker_layout(year):
    """
    Make layout with marker about films
    """
    fg_films = folium.FeatureGroup(name=f'Films {year}')

    file = open(f'Data/{year}.data', 'r', encoding='UTF8')
    out = open('out.txt', 'w', encoding='UTF8')

    film_num = {}
    for line in file:
        place, lat, lon, text = line.split('\t')
        film_num[place] = len(text.split(', '))
        fg_films.add_child(folium.Marker(location=[float(lat), float(lon)],
                                         popup=text))

    return film_num, fg_films


def color_layout(year, film_num):
    """
    Make layout with coloring country depending on films numbers
    """
    fg_color = folium.FeatureGroup(name=f'Coloring {year}')
    fg_color.add_child(folium.GeoJson(data=open('world.json', 'r',
                                      encoding='UTF-8-sig').read(),
                                      style_function=lambda x: {'fillColor': 'red' if x['properties']['NAME'] not in film_num or film_num[x['properties']['NAME']] < 5 else 'yellow' if film_num[x['properties']['NAME']] < 25 else 'green'}))

    return fg_color

map = folium.Map()

year = input()

film_num, fg_films = marker_layout(year)

fg_color = color_layout(year, film_num)

map.add_child(fg_films)
map.add_child(fg_color)
map.add_child(folium.LayerControl())
map.save('Films_map.html')

