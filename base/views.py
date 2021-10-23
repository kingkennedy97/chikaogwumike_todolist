from django.shortcuts import  redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from django.views import View
from django.shortcuts import redirect
from django.db import transaction
from googleapiclient import discovery

from .models import Task
from .forms import PositionForm

from datetime import datetime, timedelta
from base.cal_setup import get_calendar_service

import googleapiclient




class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context






class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete', 'file', 'start', 'end']
    context_object_name = 'tsks'
    success_url = reverse_lazy('tasks')

    

    def form_valid(self, form):
        form.instance.user = self.request.user

        service = get_calendar_service()
        title = str(form['title'].data)
        description = str(form['description'].data)
        begin = form['start'].data
        start = datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')
        starting = start.isoformat()

        finish = form['end'].data
        end = datetime.strptime(finish, '%Y-%m-%d %H:%M:%S')
        ending = end.isoformat()
        
        if starting == ending:
            d = datetime.now().date()
            day = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
            ending = day.isoformat()
        else:
            starting = start.isoformat()
            ending = end.isoformat()

        event_result = service.events().insert(calendarId='primary',
            body={ 
                "summary": title, 
                "description": description,
                "start": {"dateTime": starting, "timeZone": 'America/Los_Angeles'}, 
                "end": {"dateTime": ending, "timeZone": 'America/Los_Angeles'},
            }
        ).execute()

        return super(TaskCreate, self).form_valid(form)









class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'base/task_form.html'
    fields = ['title', 'description', 'complete', 'start', 'end']
    context_object_name = 'tsk'
    success_url = reverse_lazy('tasks')
    







class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))
