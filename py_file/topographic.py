# Импорт библиотеки для работы с json-файлами
# import json

# импортируем библиотеку numpy и pandas
import pandas as pd
import numpy as np

# импортируем библиотеку для работы с картами
# from keplergl import KeplerGl

# импортируем библиотеку для вычисления высоты
import srtm

# Границы полигона Иркутска
up_left = [52.446093, 103.964495]
up_right = [52.446093, 104.802521]

down_left = [52.013882, 103.964495]
down_right = [52.013882, 104.802521]


coordinates = []

coordinates.append(up_left)
coordinates.append(up_right)
coordinates.append(down_left)
coordinates.append(down_right)

headers = ['latitude', 'longitude']

df_coordinates = pd.DataFrame(coordinates, columns = headers)

generated_list_of_latitude = np.arange(down_left[0], up_left[0], 0.001)

generated_list_of_longitude = np.arange(up_left[1], up_right[1], 0.001)

# Создание пустого датафрейма
df_append = pd.DataFrame()

# Цикл по все показателям широты
for lat in range(len(generated_list_of_latitude)):
    # Создание словаря с данными. К каждой широте добавляется массив долготы
    data = {
        'latitude': generated_list_of_latitude[lat],
        'longitude': generated_list_of_longitude
    }

    df = pd.DataFrame(data)

    df_append = df_append.append(df)

print(df_append.shape)


def altitude_determinant(lat: float, lon: float) -> int:
    """
    Функция для определения высоты по координатам (широта, долгота)

    Принимает:
    lat: float - широта
    lon: float - долгота

    Возвращает:
    altitude - высота
    """
    elevation_data = srtm.get_data()
    altitude = elevation_data.get_elevation(lat, lon)
    return altitude

df_append['altitude'] = df_append.apply(lambda x: altitude_determinant(x['latitude'],x['longitude']), axis=1)

df_append.to_csv('altitude_info.csv', index=False)
