from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView


class EntrarView(LoginView):
    template_name = 'autenticacao/entrar.html'

    def form_invalid(self, form):
        try:
            user = User.objects.get(username=form.data.get('username'))
            if not user.is_active:
                messages.error(self.request, 'Usuário inativo.')
        except:
            messages.error(self.request, 'Credenciais incorretas.')
        return super().form_invalid(form)


class SairView(LogoutView):
    next_page = 'entrar'
