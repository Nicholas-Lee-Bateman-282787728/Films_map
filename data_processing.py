
def read_data():
    """
    return list with name of film, year and location from file
    """
    file = open('locations.list', 'r', encoding='ANSI')

    line = file.readline()
    while line[0] != '=':
        line = file.readline()

    data = [[cell for cell in line.strip().split('\t') if cell != ''] for line in file.readlines()]

    file.close()

    data = [[*line[0].partition(') {')[0].rpartition(' (')[::2], line[1]] for line in data if len(line) >= 2]

    return data


def data_proces(data):
    """
    Make dictionary in which keys are years, and values are dict with locations and films
    """
    data_years = {}

    for line in data:
        if line[1][:4].isdigit():
            film, year, location = line
            year = int(year[:4])
            location = location.split(',')[-1].strip()

            if year not in data_years:
                data_years[year] = {}

            if location not in data_years[year]:
                data_years[year][location] = set()
            data_years[year][location].add(film)

    return data_years


def read_locations():
    """
    Make dictionary with countries and latitude and longitude
    """
    file = open('countries.data', 'r', encoding='UTF-8')

    countries = {}
    for line in file:
       country, lat, lon = line.strip().split('\t')
       countries[country] = lat + '\t' + lon
    file.close()

    return countries


def generate_data(data_years, countries):
    """
    Make lines from every year with location name, latitude and longitude
    and all films which was made there
    """
    for year in data_years:
        file = open(f'Data/{year}.data', 'w', encoding='UTF-8')
        text = ''
        for location_name in data_years[year]:

            location = countries.get(location_name, None)
            if location is not None and len(data_years[year][location_name]) >= 3:
                text += location_name + '\t' + location + '\t' + ", ".join(sorted(list(data_years[year][location_name]))) + '\n'

        file.write(text)
        file.close()


data = read_data()
data_years = data_proces(data)
countries = read_locations()
generate_data(data_years, countries)