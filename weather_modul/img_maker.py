import cv2
from PIL import Image
from weather_modul.settings import BASE_IMG, CLOUD_IMG, RAIN_IMG, SNOW_IMG, SUN_IMG


class ImageMaker:
    """
    Риссуем открытку с погодой
    На вход принимаем словарь с данными
    Отдаём картинку, в качестве её названия выстпает дата, по которой идёт прогноз
    """

    def __init__(self, data_dict):
        self.base_image = BASE_IMG
        self.result_image = f'weather_modul/result/{str(data_dict["date"])}.jpg'
        self.cloud = CLOUD_IMG
        self.rain = RAIN_IMG
        self.snow = SNOW_IMG
        self.sun = SUN_IMG
        self.data_dict = data_dict

    def run(self):
        """

        Оснавная функция. Ищёт совпадения погоды для запуска нужного конфига, в который передаётся
        картинка погоды, цвета для градиента и при необходимости цвет, который отвечает как будет работать градиент
        """
        img = cv2.imread(self.base_image)
        if 'блач' in self.data_dict['weather']:
            self.config(img, self.cloud, 80, 90, 110)
        elif 'ождь' in self.data_dict['weather']:
            self.config(img, self.rain, 0, 0, 255, 'blue')
        elif 'нег' in self.data_dict['weather']:
            self.config(img, self.snow, 0, 204, 255, 'blue')
        elif 'олн' in self.data_dict['weather']:
            self.config(img, self.sun, 255, 255, 0)
        else:
            self.config(img, self.sun, 255, 255, 255)

    def config(self, img, weather, r, g, b, color=None):
        """
        Получаем: пустой фон, картинку погоды, ргб цвета и дополнительный цвет для правильной работы градиента
        Градиент и текст делаем с помощью cv2, после чего сохраняем картинку и уже с помощью pil вставляем картинку
        погоды

        """
        self.paste_gradient(img, r, g, b, color)
        self.paste_txt(img)
        cv2.imwrite(self.result_image, img)
        self.paste_weather_img(weather)

    def paste_weather_img(self, weather_img):
        """
        Беру картинку уже с градиентом и текстом и вствляю в неё картинку погоды
        """
        img = Image.open(self.result_image)
        cloud = Image.open(weather_img)
        img.paste(cloud, (350, 50))
        img.save(self.result_image)

    def paste_txt(self, img):
        """

        на вход беру картинку и пишу текст из словаря
        """
        x = 20
        y = 20
        for key, value in self.data_dict.items():
            y += 60
            cv2.putText(img, f'{key} : {value}', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)

    def paste_gradient(self, img, r, g, b, color=None):
        """
        Делаю градиент с помощью линий, меняя им цвет.
        Если получаем параметр цвета blue, то  в ргб палитре синий не трогаем
        """
        r = r
        g = g
        b = b
        color = color
        if color == 'blue':
            for i in range(0, 256, 1):
                cv2.line(img, (i, 0), (i, 260), (b, g, r), 1)
                if r <= 255:
                    r += 1
                if g <= 255:
                    g += 1
        else:
            for i in range(0, 256, 1):
                cv2.line(img, (i, 0), (i, 260), (b, g, r), 1)
                if b <= 255:
                    b += 1
                if r <= 255:
                    r += 1
                if g <= 255:
                    g += 1



