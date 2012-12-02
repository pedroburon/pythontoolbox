from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView, View
from django.utils.decorators import method_decorator
from django.utils import simplejson

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from guardian.decorators import permission_required

from accounts.models import Profile
from accounts.forms import UserForm


class ProfileDetailView(DetailView):
    model = Profile
    slug_url_kwarg = 'username'
    slug_field = 'user__username'

    @method_decorator(permission_required('view_profile'))
    def dispatch(self, request, username):
        return super(ProfileDetailView, self).dispatch(request, username=username)


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/user_form.html'

    @method_decorator(login_required)
    def dispatch(self, request):
        return super(ProfileUpdateView, self).dispatch(request)

    def get_success_url(self):
        return self.object.get_profile().get_update_url()

    def get_object(self):
        return self.request.user


class CurrentUserView(View):
    def get(self, request):
        user = request.user
        user_data = None
        if user.is_authenticated():
            user_data = {'username': user.username, 'fullname': user.get_full_name()}
        context = {'user': user_data}
        return HttpResponse(content=simplejson.dumps(context), content_type='application/json')
