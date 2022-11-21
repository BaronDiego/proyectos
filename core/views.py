from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.models import AnonymousUser
from django.views.generic import TemplateView

# Create your views here.
def home(request):
    return render(request, 'core/index.html')

def capex_bun(request):
    return render(request, 'core/capex_bun.html')

def ani_ctg(request):
    return render(request, 'core/ani.html')

def lote_e_bun(request):
    return render(request, 'core/lote_bun.html')

class HomeSinPrevilegios(LoginRequiredMixin, TemplateView):
    template_name = 'core/sin_privilegios.html'
    login_url = 'login'


class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin):
    raise_exception = False
    redirect_field_name = "redirect_to"
    login_url = 'login'

    def handle_no_permission(self):
        if not self.request.user == AnonymousUser():
            self.login_url = 'sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))
