# custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_car_images(car_images, car):
    return car_images.get(car, [])
