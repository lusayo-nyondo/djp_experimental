from django.http import HttpResponse
from django.urls import path
import djp

from .views import (
    index
)

urlpatterns = [
    path("", lambda request: HttpResponse("Hello world")),
    path("index", index),
] + djp.urlpatterns()
