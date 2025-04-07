from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Розширена модель користувача з додатковими полями.
    """
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('operator', 'Operator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='operator')
    is_active_duty = models.BooleanField(default=False, help_text="Чи знаходиться користувач на зміні")
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Профіль користувача"
        verbose_name_plural = "Профілі користувачів"