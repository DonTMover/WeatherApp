import datetime
import os
import tkinter
from tkinter import messagebox

import requests
from dotenv import load_dotenv


class WeatherApp:
    def _get_weather(self):
        """
        Отправляет запрос в API OpenWeatherMap и возвраает в label ответ
        :return:
        """
        load_dotenv()
        API_KEY = os.getenv('API_KEY')
        city = self.entry.get()

        url = "https://api.openweathermap.org/data/2.5/weather"
        responce = requests.get(url, params={
            'q': city,
            "units": "metric",
            "lang": 'ru',
            "appid": API_KEY
        })
        # print(responce.status_code)

        # pprint(data)
        if (responce.status_code == 200):
            data = responce.json()
            time = data["dt"]
            weather_description = data['weather'][0]['description']
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind = data['wind']['speed']
            # print(f"Температура:{temp}")
            # print(f"Как чувствуется температура: {feels_like}")
            # print(f"Влажность: {humidity}")
            # print(weather_description)
            # print(f'Скорость ветра: {wind}')

            # Convert Unix Time
            dt = datetime.datetime.fromtimestamp(time)

            # print(f'Время запроса: {dt.time()}')

            # Вытаскиваем и конвертируем время расвета и захода солнца
            sunrise = data['sys']['sunrise']
            sunrise = datetime.datetime.fromtimestamp(sunrise)
            sunset = data['sys']['sunset']
            sunset = datetime.datetime.fromtimestamp(sunset)
            result = f'Температура:{temp}°C \n Ощущается как:{feels_like}°C \n Описание:{weather_description}\n ' \
                     f'Влажность:{humidity}%\n Скорость ветра: {wind} м/с\n Время запроса: {dt}\n Время восхода: {sunrise}\n' \
                     f'Время заката: {sunset}'
            self.weather_label.config(text=result)
            # print(f'Время восхода солнца: {sunrise.time()}')
            # print(f'Время заката солнца: {sunset.time()}')

        else:
            messagebox.showwarning("Ошибка!", "Город не найден!")
        pass

    def __init__(self, root):
        self.root = root
        self.root.title("WeatherApp")

        self.main_frame = tkinter.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)
        self._create_widgets()
        self.root.resizable(False, False)

    def _create_widgets(self):
        """
        Создание графических элементов
        :return:
        """
        self.label = tkinter.Label(self.main_frame, text="Введите город: ",
                                   font=('Helvetica', 14))
        self.label.grid(row=0, column=0, padx=5)
        self.entry = tkinter.Entry(self.main_frame, font=('Helvetica', 14), justify='center')
        self.entry.grid(row=0, column=1, padx=5)

        self.btn = tkinter.Button(self.main_frame, text="Узнать погоду", font=('Helvetica', 14),
                                  command=self._get_weather)
        self.btn.grid(row=0, column=2, padx=5)
        self.weather_label = tkinter.Label(self.root, text="", font=('Helvetica', 14))
        self.weather_label.pack()


if __name__ == '__main__':
    root = tkinter.Tk()
    a = WeatherApp(root)
    root.mainloop()
