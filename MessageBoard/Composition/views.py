from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .tasks import respond_send_email, respond_accept_send_email

from .forms import *
from .models import *


class StartPage(ListView):
    model = Advert
    template_name = 'startpage.html'
    context_object_name = 'adverts'


class AdvertCreate(LoginRequiredMixin, CreateView):
    model = Advert
    template_name = 'advert_create.html'
    form_class = AdvertForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm('Composition.add_advert'):
            return HttpResponseRedirect(reverse('account_profile'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form, advert=None):
        advert = form.save(commit=False)
        advert.author = User.objects.get(id=self.request.user.id)
        advert.save()
        return super().form_valid(form)


class AdvertUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'Composition.change_advert'
    template_name = 'advert_create.html'
    form_class = AdvertForm
    success_url = '/update/'

    def dispatch(self, request, *args, **kwargs):
        author = Advert.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Редактировать объявление может только его автор")

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advert.objects.get(pk=id)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/advert/' + str(self.kwargs.get('pk')))


class AdvertDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'Composition.delete_advert'
    model = Advert
    template_name = 'advert_delete.html'
    success_url = reverse_lazy('start_page')

    def dispatch(self, request, *args, **kwargs):
        author = Advert.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Удалить объявление может только его автор")


class AdvertDetail(DetailView):
    model = Advert
    template_name = 'advert_detail.html'
    context_object_name = 'advert'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Response.objects.filter(author_id=self.request.user.id).filter(advert_id=self.kwargs.get('pk')):
            context['respond'] = "Откликнулся"
        elif self.request.user == Advert.objects.get(pk=self.kwargs.get('pk')).author:
            context['respond'] = "Мое объявление"
        return context


title = str("")


class Responses(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'responses.html'
    context_object_name = 'responses'

    def get_context_data(self, **kwargs):
        context = super(Responses, self).get_context_data(**kwargs)
        global title
        if self.kwargs.get('pk') and Advert.objects.filter(id=self.kwargs.get('pk')).exists():
            title = str(Advert.objects.get(id=self.kwargs.get('pk')).title)
            print(title)
        context['form'] = ResponsesFilterForm(self.request.user, initial={'title': title})
        context['title'] = title
        if title:
            advert_id = Advert.objects.get(title=title)
            context['filter_responses'] = list(Response.objects.filter(advert_id=advert_id).order_by('-createDate'))
            context['response_advert_id'] = advert_id.id
        else:
            context['filter_responses'] = list(
                Response.objects.filter(advert_id__author_id=self.request.user).order_by('-createDate')
            )
        context['myresponses'] = list(Response.objects.filter(author_id=self.request.user).order_by('-createDate'))
        return context

    def advert(self, request, *args, **kwargs):
        global title
        title = self.request.POST.get('title')
        if self.kwargs.get('pk'):
            return HttpResponseRedirect('/responses')
        return self.get(request, *args, **kwargs)



@login_required
def response_accept(request, **kwargs):
    if request.user.is_authenticated:
        response = Response.objects.get(id=kwargs.get('pk'))
        response.status = True
        response.save()
        respond_accept_send_email.delay(response_id=response.id)
        return HttpResponseRedirect('/responses')
    else:
        return HttpResponseRedirect('/accounts/login')


@login_required
def response_delete(request, **kwargs):
    if request.user.is_authenticated:
        response = Response.objects.get(id=kwargs.get('pk'))
        response.delete()
        return HttpResponseRedirect('/responses')
    else:
        return HttpResponseRedirect('/accounts/login')


class Respond(LoginRequiredMixin, CreateView):
    model = Response
    template_name = 'respond.html'
    form_class = ResponseForm
    success_url = reverse_lazy('start_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        respond = form.save(commit=False)
        respond.author = User.objects.get(id=self.request.user.id)
        respond.advert = Advert.objects.get(id=self.kwargs.get('pk'))
        respond.save()
        respond_send_email.delay(respond_id=respond.id)
        return redirect(f'/advert/{self.kwargs.get("pk")}')

