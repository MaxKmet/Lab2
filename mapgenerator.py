import pandas as pd
import geocoder
import folium


def get_location_df(filename, location):
    '''
    (str, str) -> pandas.DataFrame
    Returns a pd dataframe about movies in
    a given location based on a given csv file
    '''
    df = pd.read_csv(filename, error_bad_lines=False)
    df = df.dropna()
    df = df[df['year'].apply(lambda x: x.isnumeric())]
    df = df[df['location'].apply(lambda x: location in x)]
    df['year'] = pd.to_numeric(df['year'])
    return df


def get_year_df(filename, year):
    '''
    (str, int) -> pandas.DataFrame
    Returns a pd dataframe about movies in
    a given year based on a given csv file
    '''
    df = pd.read_csv(filename, error_bad_lines=False)
    df = df.dropna()
    df = df[df['year'].apply(lambda x: x.isnumeric())]
    df['year'] = pd.to_numeric(df['year'])
    df = df[df['year'] == year]
    return df


def get_movie_df(filename, moviename):
    '''
    (str, str) -> pandas.DataFrame
    Returns a pd dataframe about a given movie
    based on a given csv file
    '''
    df = pd.read_csv(filename, error_bad_lines=False)
    df = df.dropna()
    df = df[df['year'].apply(lambda x: x.isnumeric())]
    df['year'] = pd.to_numeric(df['year'])
    movie_df = df[df['movie'] == moviename]
    return movie_df


def get_coordinates(locations, num_first=None):
    '''
    (list of strings) -> array of lists(latitude, longitude)
    Takes list of names of locations and returns
    array of numeric pairs(longitude, latitude)
    '''
    coordinates = []
    print("Coordinates calculation progress: ")
    for location in locations[:num_first]:
        print(geocoder.arcgis(location).latlng)
        coordinates.append(geocoder.arcgis(location).latlng)
    return coordinates


def generate_map(filename, outfile, year, movie, area_middle_treshhold, area_middle_treshhold_upper, num_first):
    '''
    (str, str, int, str, int, int, int) -> None
    Generates interactive html map based on input parameters
    '''
    map = folium.Map()
    # 1895 - year when Lumiere brothers created first films
    year_df = get_year_df(filename, year)
    locations_year = year_df['location'].values
    movies_year = year_df['movie'].values
    coordinates_year = get_coordinates(locations_year, num_first)

    fg_year = folium.FeatureGroup(name="Films in " + str(year))
    for ind, coord in enumerate(coordinates_year):
        if coord:
            fg_year.add_child(folium.CircleMarker(location=coord,
                                                  radius=10,
                                                  popup=movies_year[ind] +
                                                  "(" + str(year) + ")",
                                                  fill_color="green",
                                                  color="green",
                                                  fill_opacity=0.5))

    movie_df = get_movie_df(filename, movie)
    locations_movie = movie_df['location'].values
    coordinates_movie = get_coordinates(locations_movie, num_first)

    fg_movie = folium.FeatureGroup(name=movie + " Locations")
    for ind, coord in enumerate(coordinates_movie):
        fg_movie.add_child(folium.CircleMarker(location=coord,
                                               radius=10,
                                               popup=locations_movie[ind] + "(" + movie + ")",
                                               fill_color="blue",
                                               color="blue",
                                               fill_opacity=0.5))

    fg_area = folium.FeatureGroup(name="Country Area Info")

    fg_area.add_child(folium.GeoJson(data=open('world.json', 'r',
                                               encoding='utf-8-sig').read(),
                                     style_function=lambda x: {'fillColor': 'green'
                                                               if x['properties']['AREA'] < area_middle_treshhold
                                                               else 'orange' if area_middle_treshhold <= x['properties']['AREA'] < area_middle_treshhold_upper
                                                               else 'red'}))

    map.add_child(fg_area)
    map.add_child(fg_movie)
    map.add_child(fg_year)

    map.add_child(folium.LayerControl())
    map.save(outfile)


def get_parameter(parameter):
    '''
    (str) -> str
    Returns a parameter for generate_map based on user input
    '''
    temp_parameter = input()
    if temp_parameter:
        if temp_parameter == "None":
            return None
        parameter = temp_parameter
    return parameter


if __name__ == "__main__":

    dataset_src = "locations.csv"
    year = 1895
    movie = "Inception "
    # нижня межа площі з якої починається розфарбування в жовтий minimum country area threshhold where paint country in yellow
    area_middle_treshhold = 200000
    # верхня межа площі з якої починається розфарбування в жовтий max country area threshhold where paint in yellow stops
    area_middle_treshhold_upper = 700000
    outfile = "SampleMap.html"
    num_first = 10  # кількість перших значень по кожному з параметрів (None щоб вивести всі)

    print("Цей додаток генерує інтерактивні карти")
    print("\nДЛЯ ГЕНЕРАЦІЇ КАРТИ З ПАРАМЕТРАМИ ЗА ЗАМОВЧУВАННЯМ ВВЕДІТЬ 1\nДЛЯ ВВЕДЕННЯ ПАРАМЕТРІВ ВРУЧНУ ВВЕДІТЬ 0\nПараметри за замовчуванням:")
    print("Місце розташування даних: "+dataset_src)
    print("Фільми року випуску: "+str(year))
    print("Нижня межа площі країни(км.кв) з якої починається розфарбування в жовтий: " +
          str(area_middle_treshhold))
    print("Верхня межа площі країни(км.кв) після якої закінчується розфарбування в жовтий: " +
          str(area_middle_treshhold_upper))
    print("Місце розташування вихідного html файлу: " +
          str(outfile))
    print("Кількість перших значень для виводу по кожноу з параметрів(Бажано невелике): " +
          str(num_first))
    print("Ввід: ")
    input_parameter = int(input())
    if input_parameter == 1:
        generate_map(dataset_src, outfile, year, movie, area_middle_treshhold,
                     area_middle_treshhold_upper, num_first)
    elif input_parameter == 0:
        print("РЕЖИМ РУЧНОГО ВВОДУ\nЩОБ ВИКОРИСТОВУВАТИ ЗНАЧЕННЯ ДАНОГО ПАРАМЕТРУ ЗА ЗАМОВЧУВАННЯМ НАТИСНІТЬ Enter:\n\n")
        print("Введіть місце розташування даних(або Enter):\n")
        dataset_src = get_parameter(dataset_src)
        print("Введіть рік випуску фільмів(або Enter):\n")
        year = int(get_parameter(year))
        print("Введіть назву фільму(або Enter):\n")
        movie = get_parameter(movie) + " "
        print("Введіть нижню межу площі країни для розфарбовки її в жовтий(або Enter):\n")
        area_middle_treshhold = int(get_parameter(area_middle_treshhold))
        print("Введіть верхню межу площі країни для розфарбовки її в жовтий(або Enter):\n")
        area_middle_treshhold_upper = int(get_parameter(area_middle_treshhold_upper))
        print("Введіть шлях до вихідного html файлу(або Enter):\n")
        outfile = get_parameter(outfile)
        print("Введіть кількість перших значень для виводу по кожноу з параметрів(Бажано невелике) або None, щоб вивести всі\n")
        num_first_t = get_parameter(num_first)
        num_first = int(num_first_t) if num_first_t else None
        generate_map(dataset_src, outfile, year, movie, area_middle_treshhold,
                     area_middle_treshhold_upper, num_first)

    else:
        print("Error: Input must be 0 or 1")
