from django.shortcuts import render , redirect
import re
from goods.models import GoodsType
# Create your views here.

def index(request):
    """注册页"""
    return render(request, "goods/index.html")
