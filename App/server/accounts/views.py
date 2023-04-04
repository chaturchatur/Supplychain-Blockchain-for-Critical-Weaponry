from django.contrib.auth.views import LoginView

# Create your views here.
class UserLogin(LoginView):
    template_name = 'login.html'
