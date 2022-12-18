from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Author, Category, Post, Comment
from .filters import PostFilter
from .forms import PostForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect


class NewsList(ListView):
    model = Post
    template_name = 'news_list.html'
    ordering = '-date_created'
    context_object_name = "news_list"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        current_url = self.request.path
        if current_url.split('/')[1] == 'news':
            self.filterset = PostFilter(self.request.GET, queryset.filter(categoryType=Post.NEWS))
        else:
            self.filterset = PostFilter(self.request.GET, queryset.filter(categoryType=Post.ARTICLE))
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsSearch(NewsList):
    template_name = 'news_search.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        current_url = self.request.path
        post = form.save(commit=False)

        if current_url.split('/')[1] == 'news':
            post.categoryType = self.model.NEWS
        else:
            post.categoryType = self.model.ARTICLE

        self.object = form.save()
        redirectURL = '/' + current_url.split('/')[1] + '/' + str(self.object.id)
        return redirect(redirectURL)


class NewsEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    def post(self, request, *args, **kwargs):
        current_url = self.request.path
        redirectURL = ''
        for i in current_url.split('/'):
            if i == 'edit':
                redirectURL = redirectURL[:-1]
                break
            redirectURL += i + '/'
        super().post(request, *args, **kwargs)
        return redirect(redirectURL)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    #permission_required = ('news.delete_post',)

    def post(self, request, *args, **kwargs):
        current_url = self.request.path
        redirectURL = ''
        tempURL = ''
        for i in current_url.split('/'):
            if i == 'delete':
                redirectURL = tempURL[:-1]
                break
            else:
                tempURL = redirectURL
            redirectURL += i + '/'
        super().post(request, *args, **kwargs)
        return redirect(redirectURL)


class ProfileEdit(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = User
    template_name = 'profile_edit.html'