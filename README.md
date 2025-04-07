# Система розпізнавання об'єктів з БПЛА

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django: 4.2](https://img.shields.io/badge/Django-4.2-green.svg)
![YOLOv5](https://img.shields.io/badge/YOLOv5-latest-orange.svg)

## Опис проєкту

Веб-платформа для розпізнавання людей, автомобілів та військової техніки на фото та відео з використанням Django та Python. Система обробляє як завантажені файли, так і відеопотік з БПЛА в реальному часі. Орієнтована на невелику кількість користувачів (1-2) та оптимізована для роботи на середньостатистичному ноутбуці.

## Функціональні можливості

- Автентифікація користувачів (адміністратор та оператор)
- Робота з потоковим відео з БПЛА в реальному часі (RTSP, RTMP)
- Завантаження та обробка фото і відео файлів (JPG, PNG, MP4)
- Розпізнавання та класифікація людей, автомобілів та військової техніки
- Візуалізація результатів з підсвічуванням знайдених об'єктів
- Збереження та експорт результатів розпізнавання

## Технічний стек

- **Backend**: Django 4.2, Python 3.10+, SQLite
- **AI/ML**: YOLOv5, PyTorch, OpenCV
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Інші технології**: WebSockets для стрімінгу, AJAX для оновлення даних

## Вимоги до системи

- Python 3.10 або новіше
- 8 GB RAM (мінімум)
- NVIDIA GPU з підтримкою CUDA (опціонально, для кращої продуктивності)
- Веб-камера або підключення до БПЛА з відеотрансляцією

## Інструкція з встановлення та розгортання

### Крок 1: Клонування репозиторію

```bash
git clone https://github.com/yourusername/drone-object-detection.git
cd drone-object-detection
```

### Крок 2: Створення та активація віртуального середовища

```bash
# Створення віртуального середовища
python -m venv venv

# Активація віртуального середовища
# Для Windows:
venv\Scripts\activate
# Для macOS/Linux:
source venv/bin/activate
```

### Крок 3: Встановлення залежностей

```bash
# Встановлення основних залежностей
pip install -r requirements.txt

# Встановлення PyTorch з підтримкою CUDA (опціонально)
# Перейдіть на https://pytorch.org/get-started/locally/ для отримання команди,
# яка відповідає вашій ОС та версії CUDA
```

### Крок 4: Налаштування Django проєкту

```bash
# Створення міграцій
python manage.py makemigrations

# Застосування міграцій
python manage.py migrate

# Створення суперкористувача (адміністратора)
python manage.py createsuperuser
```

### Крок 5: Завантаження попередньо навченої моделі YOLO

```bash
# Завантаження YOLOv5s
python -c "from detector.utils import download_model; download_model('yolov5s')"
```

### Крок 6: Запуск сервера розробки

```bash
python manage.py runserver
```

Після цього веб-інтерфейс буде доступний за адресою `http://127.0.0.1:8000/`.

## Поетапний план реалізації проєкту

### Етап 1: Налаштування базової інфраструктури Django (1-2 дні)

#### 1.1. Створення проєкту та базових додатків

```bash
# Створення проєкту Django
django-admin startproject drone_detection

# Створення додатків
cd drone_detection
python manage.py startapp accounts
python manage.py startapp stream_handler
python manage.py startapp upload_handler
python manage.py startapp detector
python manage.py startapp dashboard
```

#### 1.2. Налаштування структури проєкту

- Додайте створені додатки до `INSTALLED_APPS` в `settings.py`
- Налаштуйте базову маршрутизацію в `urls.py`
- Створіть базову структуру шаблонів та статичних файлів

#### 1.3. Реалізація системи автентифікації

- Створіть моделі користувачів з ролями (адміністратор, оператор)
- Реалізуйте форми реєстрації та авторизації
- Налаштуйте відповідні представлення та шаблони

### Етап 2: Імплементація розпізнавання об'єктів (3-5 днів)

#### 2.1. Інтеграція YOLOv5

```bash
# Створіть директорію для моделей
mkdir -p detector/models

# Створіть скрипт для завантаження моделей
touch detector/utils.py
```

- Напишіть функції для завантаження попередньо навчених моделей YOLOv5
- Реалізуйте базовий клас для розпізнавання об'єктів

#### 2.2. Тестування та налаштування базової моделі

- Створіть тестовий скрипт для перевірки розпізнавання на статичних зображеннях
- Налаштуйте параметри моделі для оптимального балансу швидкості та точності
- Реалізуйте функції для обробки результатів розпізнавання

#### 2.3. Дотренування моделі для військової техніки

- Підготуйте або знайдіть датасет з військовою технікою (можна використати [Roboflow](https://roboflow.com/))
- Напишіть скрипт для fine-tuning моделі:

```python
# Приклад скрипта для fine-tuning (detector/training.py)
import torch
from detector.models import get_yolo_model

def fine_tune_model(data_yaml, epochs=10, batch_size=16):
    model = get_yolo_model('yolov5s')
    model.train(data=data_yaml, epochs=epochs, batch_size=batch_size)
    return model
```

### Етап 3: Розробка системи обробки відеопотоку (3-4 дні)

#### 3.1. Підключення до джерел відео

- Реалізуйте клас для роботи з різними джерелами відео (файл, веб-камера, RTSP/RTMP потік)
- Створіть функціонал для буферизації кадрів

```python
# Приклад в stream_handler/video_stream.py
import cv2

class VideoStream:
    def __init__(self, source, buffer_size=10):
        self.source = source
        self.buffer_size = buffer_size
        self.cap = None
        
    def connect(self):
        self.cap = cv2.VideoCapture(self.source)
        return self.cap.isOpened()
    
    def read_frame(self):
        if not self.cap.isOpened():
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame
    
    def close(self):
        if self.cap is not None:
            self.cap.release()
```

#### 3.2. Реалізація WebSocket для трансляції в реальному часі

- Використайте Django Channels для реалізації WebSocket
- Налаштуйте асинхронну обробку відеопотоку

```bash
# Встановлення Django Channels
pip install channels
pip install channels_redis
```

- Створіть consumers.py та routing.py для обробки WebSocket

#### 3.3. Інтеграція розпізнавання з відеопотоком

- Реалізуйте логіку обробки кадрів та розпізнавання об'єктів в реальному часі
- Оптимізуйте процес для зменшення навантаження (обробка кожного 2-3 кадру)

### Етап 4: Створення веб-інтерфейсу (3-4 дні)

#### 4.1. Розробка базових шаблонів

- Створіть базовий шаблон з використанням Bootstrap 5
- Реалізуйте головну сторінку та сторінку дашборду

#### 4.2. Сторінка перегляду відеопотоку з розпізнаванням

- Розробіть інтерфейс для відображення відео з мітками об'єктів
- Реалізуйте панель налаштувань для керування процесом розпізнавання

#### 4.3. Сторінка завантаження та обробки файлів

- Створіть форму для завантаження фото та відео
- Реалізуйте логіку обробки завантажених файлів

#### 4.4. Сторінка історії та результатів

- Розробіть інтерфейс для перегляду історії сесій
- Реалізуйте функціонал експорту результатів в CSV/JSON

### Етап 5: Оптимізація продуктивності (2-3 дні)

#### 5.1. Профілювання та виявлення "вузьких місць"

- Використайте інструменти профілювання Python для виявлення повільних ділянок коду
- Проаналізуйте використання пам'яті та CPU

#### 5.2. Оптимізація розпізнавання

- Реалізуйте динамічне налаштування якості розпізнавання залежно від потужності пристрою
- Додайте перемикач між режимами якості (висока точність / висока швидкість)

#### 5.3. Тестування в різних умовах

- Перевірте роботу на різних пристроях
- Проведіть тестування з різними джерелами відео

## Структура проєкту

```
drone_detection/
│
├── accounts/                    # Додаток для управління користувачами
│   ├── models.py                # Моделі користувачів та ролей
│   ├── views.py                 # Представлення авторизації
│   └── templates/               # Шаблони авторизації
│
├── stream_handler/              # Додаток для роботи з відеопотоком
│   ├── video_stream.py          # Класи для роботи з різними джерелами відео
│   ├── consumers.py             # WebSocket consumers
│   └── routing.py               # Маршрутизація WebSocket
│
├── upload_handler/              # Додаток для завантаження файлів
│   ├── models.py                # Моделі для зберігання медіафайлів
│   └── views.py                 # Представлення для завантаження та обробки
│
├── detector/                    # Додаток для розпізнавання об'єктів
│   ├── models/                  # Директорія для моделей YOLO
│   ├── utils.py                 # Утиліти для роботи з моделями
│   ├── detector.py              # Класи розпізнавання об'єктів
│   └── training.py              # Скрипти для дотренування моделей
│
├── dashboard/                   # Додаток для веб-інтерфейсу
│   ├── views.py                 # Основні представлення
│   └── templates/               # Шаблони інтерфейсу
│
├── static/                      # Статичні файли (CSS, JS, зображення)
│
├── templates/                   # Загальні шаблони
│
├── manage.py                    # Скрипт управління Django
├── requirements.txt             # Залежності проєкту
└── README.md                    # Документація проєкту
```

## Додаткові рекомендації

1. **Датасети для військової техніки:**
   - [Military Vehicles and Equipment Dataset](https://www.kaggle.com/datasets/military-vehicles)
   - [Roboflow Military Vehicles](https://universe.roboflow.com/search?q=military)

2. **Оптимізація для роботи на ноутбуці:**
   - Використовуйте YOLOv5s (small) для балансу швидкості та точності
   - Зменшіть роздільну здатність відео для обробки (640x480)
   - Встановіть частоту обробки 5-10 кадрів на секунду

3. **Тестування без БПЛА:**
   - Використовуйте веб-камеру ноутбука для тестування
   - Використовуйте записані відео з БПЛА

## Вирішення потенційних проблем

1. **Низька продуктивність при розпізнаванні:**
   - Зменшіть роздільну здатність обробки
   - Збільшіть інтервал між кадрами обробки
   - Використовуйте більш легку модель (YOLOv5n)

2. **Помилки підключення до БПЛА:**
   - Перевірте налаштування RTSP/RTMP
   - Використовуйте буферизацію для стабільного потоку
   - Додайте механізм повторного підключення

3. **Проблеми з розгортанням на різних платформах:**
   - Використовуйте Docker для стандартизації середовища
   - Створіть детальну інструкцію для різних операційних систем

## Ліцензія

MIT License

## Контакти

Якщо у вас виникли питання або пропозиції, створіть Issue в цьому репозиторії або зв'яжіться з автором.
