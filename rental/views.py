from django.shortcuts import render
from django.template.defaulttags import register
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from models import Device, Event, Inventory
from django.contrib.auth.models import User
# Create your views here.

@register.filter(name='lookup')
def cut(value, arg):
    return value[arg]


def devices(request, event_slug):
  event = Event.objects.get(slug=event_slug)
  devices = Device.objects.all()
  event_inventory = Inventory.objects.filter(event=event)
  inventories = {}
  for device in devices:
      #taking all the stock
      inventories[device.name] = event_inventory.filter(device=device)

  content = {
    'event' : event,
    'devices' : devices,
    'inventories' : inventories
  }
  return render(request,'devices.html', content)

def view_device(request, event_slug, device_name):
  device = Device.objects.get(name=device_name)
  event = Event.objects.get(slug=event_slug)

  content = {
    'event' : event,
    'device' : device
  }
  return render(request,'view_device.html', content)

def home(request):
  content = {
    'events' : Event.objects.all()
  }
  return render(request,'events.html', content)

#custom view to see where all the hardware are located
def hardware_location(request):
    inventories = {}
    free_inventories = {}
    for event in Event.objects.all():
        event_inventory = Inventory.objects.filter(event=event)
        inventories[event.name] = {}
        for device in Device.objects.all():
            inventories[event.name][device.name] = event_inventory.filter(device=device)

    unassigned_inventory = Inventory.objects.filter(event=None)
    for device in Device.objects.all():
        free_inventories[device.name] = unassigned_inventory.filter(device=device)

    return render(request,'hardware_location.html', {'inventories': inventories, 'free_inventories': free_inventories})

def user_settings(request, user_name):
  user = User.objects.get(username = user_name)

  content = {
    'user' : user
  }

  return render(request,'user_profile.html', content)
