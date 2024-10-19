from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Comments, Tags, Category
from .forms import CreatePostForm, UpdatePostForm, CommentsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class PostListView(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_individual.html'
    context_object_name = 'posts'
    pk_url_kwarg = 'id'
    # Redundante porque DetailView lo usara por defecto.
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm()
        context['comments'] = Comments.objects.filter(
            post_id=self.kwargs['id'])
        return context

    def post(self, request, *args, **kwargs):
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # comment.user_id=request.user_id
            comment.user = request.user
            comment.post_id = self.kwargs['id']
            comment.save()
            return redirect('apps.posts:post_individual', id=self.kwargs['id'])
            # return redirect('apps:post_individual', id=self.kwargs['id'])
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
            # return render(request, 'some_template.html', context)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comments
    form_class = CommentsForm
    template_name = 'posts/comments_create.html'
    success_url = 'posts/comments'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)


class PostCreateView(CreateView):
    form_class = CreatePostForm
    template_name = 'posts/post_create.html'
    model = Post
    success_url = reverse_lazy('apps.posts:posts')


class PostUpdateView(UpdateView):
    form_class = UpdatePostForm
    template_name = 'posts/post_update.html'
    model = Post
    success_url = reverse_lazy('apps.posts:posts')
    pk_url_kwarg = 'id'


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('apps.posts:posts')
    pk_url_kwarg = 'id'

# Lista de Categorías


class CategoryListView(ListView):
    model = Category
    template_name = 'posts/category.html'
    context_object_name = 'categorys'


# Borrar Categorías


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'posts/category_delete.html'
    success_url = reverse_lazy('apps.posts:category')

# post por categorias


class PostCategoryView(ListView):
    model = Post
    template_name = 'posts/post_category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(category_id=self.kwargs['pk'])


# Tags


class TagsListView(ListView):
    model = Tags
    template_name = 'taglist.html'
    context_object_name = 'tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tags.objects.all()
        context['tags'] = Tags.objects.get(id=self.kwargs['pk'])
        return context
