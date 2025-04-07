from django.db import models


class SystemSettings(models.Model):
    """
    Налаштування системи.
    """
    detection_confidence = models.FloatField(default=0.45, help_text="Поріг впевненості виявлення (від 0 до 1)")
    iou_threshold = models.FloatField(default=0.45, help_text="Поріг IOU для NMS (від 0 до 1)")
    max_detection_count = models.IntegerField(default=100, help_text="Максимальна кількість об'єктів для виявлення")

    # Налаштування продуктивності
    use_gpu = models.BooleanField(default=True, help_text="Використовувати GPU для розпізнавання")
    processing_resolution = models.CharField(
        max_length=20,
        choices=[
            ('low', '640x480'),
            ('medium', '1280x720'),
            ('high', '1920x1080'),
        ],
        default='medium',
        help_text="Роздільна здатність для обробки"
    )

    # Одиночний запис налаштувань
    class Meta:
        verbose_name = "Налаштування системи"
        verbose_name_plural = "Налаштування системи"

    def save(self, *args, **kwargs):
        # Забезпечуємо, що буде тільки один запис
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        # Завантаження єдиного запису або створення його
        obj, created = cls.objects.get_or_create(pk=1)
        return obj