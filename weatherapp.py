import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel
from PyQt5.QtCore import Qt, QTimer
import os


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name:  ", self)
        self.city_name = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature = QLabel(self)
        self.emoji = QLabel(self)
        self.description_lable = QLabel(self)
        self.title = "🌍 World Weather App 🌍 " 
        self.index = 0
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(600, 400, 400, 300)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_title)
        self.timer.start(300) 
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_name)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature)
        vbox.addWidget(self.emoji)
        vbox.addWidget(self.description_lable)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_name.setAlignment(Qt.AlignCenter)
        self.temperature.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.description_lable.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_lable")
        self.city_name.setObjectName("city_name")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature.setObjectName("temperature")
        self.emoji.setObjectName("emoji")
        self.description_lable.setObjectName("description_lable")

        self.get_weather_button.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet("""
                    QLabel, QPushButton{
                           font-family:calibri;
                           }
                    QLabel#city_lable{
                           font-size:40px;
                           font-style: italic;
                           }
                    QLineEdit#city_name{
                           font-size:30px;
                           }
                    QPushButton#get_weather_button{
                           font-size:30px;
                           border-radius: 20px;
                           font-weight:bold;
                           background-color: green;
                    
                           }
                                               
                    QLabel#temperature{
                           font-size:70px;
                           font-weight:bold;
                           }
                    QLabel#emoji{
                           font-size:100px;
                           font-family: Segeo UI emoji;}
                    QLabel#description_lable{
                           font-size:50px;
                           font-weight:bold;}

                            """)
        self.get_weather_button.clicked.connect(self.get_weather)
    def get_weather(self):
        api_key = os.getenv("API_KEY")
        city_name = self.city_name.text()
        base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        try:
            response = requests.get(base_url)
            response.raise_for_status()
            data = response.json()
            if data['cod'] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_errors("Bad requests\n Please check your input")
                case 401:
                    self.display_errors("Unauthorized acces\n")
                case 403:
                    self.display_errors("Forbidden")
                case 404:
                    self.display_errors(" City Not found")
                case 500:
                    self.display_errors("internal server error")
                case 502:
                    self.display_errors("Bad gateway")
                case 503:
                    self.display_errors("Service unavailable")
                case 504:
                    self.display_errors("Gateway timeout")
                case _:
                    self.display_weather(f"HTTPError occured, {http_error}")
        except requests.exceptions.ConnectionError:
            self.display_errors("Connection lost \n check your internet")
        except requests.exceptions.ConnectTimeout:
            self.display_errors("Connection timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_errors("The page redirected too many times")
        except requests.exceptions.RequestException as req_error:
            self.display_errors(f"Request failed {req_error}")
              
    def display_errors(self, error_message):
        self.temperature.setStyleSheet("font-size:30px;" "color:red;")
        self.temperature.setText(error_message)

    def display_weather(self, data):
        temperature_in_kelvin = data["main"]["temp"]
        temperature_in_celcious = temperature_in_kelvin - 273.15
        temperature_in_ferenheit = (temperature_in_kelvin * 9/5) - 459.67
        weather_desc = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]
        self.temperature.setText(f"{temperature_in_celcious: .0f} °C") 
        self.emoji.setText(self.get_weather_emoji(weather_id))
        self.description_lable.setText(weather_desc)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200<= weather_id <=232:
            return "⛈️"
        elif 300<= weather_id <= 321:
            return "☁️"
        elif 500 <= weather_id<=531:
            return "⛈️"
        elif 600 <=weather_id<=622:
            return "🌨️"
        elif 701<=weather_id<=741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "🍃"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801<=weather_id<=804:
            return "☁️"
        else:
            return ""


    def scroll_title(self):
        # Scroll title by shifting characters left to right
        self.index = (self.index + 1) % len(self.title)
        new_title = self.title[self.index:] + self.title[:self.index]
        self.setWindowTitle(new_title)

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())