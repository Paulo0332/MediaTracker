import random
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .quotes import CHARACTERS_LIST
# Create your views here.

class CustomLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_node = random.choice(CHARACTERS_LIST)
        context["selected_character"] = selected_node
        return context