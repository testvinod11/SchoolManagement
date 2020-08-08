from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def handler404(self):
    self.template_name = '404.html'
    response = self.render_to_response(context={})
    response.status_code = 404
    return response


class CommonContextData():
    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        return super().get_context_data(view_for=self.view_for, **kwargs)


class CommonCreateView(CreateView, CommonContextData):
    template_name = 'registration/create.html'
    fields = ('name', )


class CommonListView(ListView):

    template_name = 'registration/list.html'
    context_object_name = 'queryset'
    paginate_by = 10
    view_for = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(queryset, self.paginate_by)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        context['queryset'] = queryset
        context["view_for"] = self.view_for
        return context

    def get_queryset(self):
        return super().get_queryset().order_by('-id').values('id', 'name')


class CommonDetailView(DetailView):
    template_name = 'registration/detail.html'
    context_object_name = 'object'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CommonUpdateView(UpdateView, CommonContextData):

    template_name = 'registration/update.html'
    context_object_name = 'student'
    fields = ('name',)
    # view_for = ""

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)


class CommonDeleteView(DeleteView, CommonContextData):
    template_name = 'registration/delete.html'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)
