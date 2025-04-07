from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import SystemSettings
from detector.models import DetectionResult, DetectionSession
from stream_handler.models import StreamSettings


@login_required
def index_view(request):
    """
    Головна сторінка дашборду.
    """
    # Отримуємо статистику розпізнавань за останні 7 днів
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_detections = DetectionResult.objects.filter(
        detection_time__gte=seven_days_ago
    ).order_by('-detection_time')

    # Отримуємо статистику по типах об'єктів
    object_types = DetectionResult.objects.values('object_type').distinct()

    # Отримуємо останні сесії розпізнавання
    recent_sessions = DetectionSession.objects.all().order_by('-start_time')[:5]

    context = {
        'recent_detections': recent_detections[:10],  # Останні 10 розпізнавань
        'object_types': object_types,
        'recent_sessions': recent_sessions,
        'detection_count': DetectionResult.objects.count(),
        'session_count': DetectionSession.objects.count(),
    }

    return render(request, 'dashboard/index.html', context)


@login_required
def realtime_view(request):
    """
    Інтерфейс для роботи з відео в реальному часі.
    """
    # Отримуємо налаштування потоку
    stream_settings = StreamSettings.objects.first()

    context = {
        'stream_settings': stream_settings,
    }

    return render(request, 'dashboard/realtime.html', context)


@login_required
def history_view(request):
    """
    Сторінка історії розпізнавань.
    """
    # Отримуємо всі сесії розпізнавання
    sessions = DetectionSession.objects.all().order_by('-start_time')

    context = {
        'sessions': sessions,
    }

    return render(request, 'dashboard/history.html', context)


@staff_member_required
def settings_view(request):
    """
    Сторінка налаштувань системи.
    Доступна тільки для адміністраторів.
    """
    settings = SystemSettings.load()

    if request.method == 'POST':
        # Оновлення налаштувань
        settings.detection_confidence = float(request.POST.get('detection_confidence', 0.45))
        settings.iou_threshold = float(request.POST.get('iou_threshold', 0.45))
        settings.max_detection_count = int(request.POST.get('max_detection_count', 100))
        settings.use_gpu = request.POST.get('use_gpu') == 'on'
        settings.processing_resolution = request.POST.get('processing_resolution', 'medium')
        settings.save()
        return redirect('dashboard:settings')

    context = {
        'settings': settings,
    }

    return render(request, 'dashboard/settings.html', context)


@login_required
def get_detection_stats(request):
    """
    API для отримання статистики розпізнавань для графіків.
    """
    # Статистика по днях за останній тиждень
    seven_days_ago = timezone.now() - timedelta(days=7)
    daily_stats = []

    for i in range(7):
        day = seven_days_ago + timedelta(days=i)
        next_day = day + timedelta(days=1)
        count = DetectionResult.objects.filter(
            detection_time__gte=day,
            detection_time__lt=next_day
        ).count()
        daily_stats.append({
            'date': day.strftime('%Y-%m-%d'),
            'count': count
        })

    # Статистика по типах об'єктів
    object_type_stats = {}
    for result in DetectionResult.objects.all():
        if result.object_type in object_type_stats:
            object_type_stats[result.object_type] += 1
        else:
            object_type_stats[result.object_type] = 1

    object_stats = [
        {'type': obj_type, 'count': count}
        for obj_type, count in object_type_stats.items()
    ]

    return JsonResponse({
        'daily_stats': daily_stats,
        'object_stats': object_stats,
    })