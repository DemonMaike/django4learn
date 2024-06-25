from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

def post_share(request, post_id):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             id=post_id)

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f'{cd["name"]} recommends you read {post.title}'
            message = f'Read {post.title} at {post_url}\n\n{cd["name"]}\'s comments:{cd["comments"]}'
            send_mail(subject, message, 'dd89268147556@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
