from django.shortcuts import render
from .models import Blog

def blog_list(request):
    """
    View to display all blog posts
    """
    blogs = Blog.objects.all().order_by('-created_at')  # newest first
    context = {
        'blogs': blogs
    }
    return render(request, 'user/blog_list.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.paginator import Paginator

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    comments_list = blog.comments.all().order_by('-created_at')

    # Pagination: 5 comments per page
    paginator = Paginator(comments_list, 5)
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.user = request.user
                comment.save()
                # redirect to last page to show newly added comment
                return redirect(f'{request.path}?page={paginator.num_pages}')
        else:
            messages.error(request,'Sory!. You must login to add comments to our blog')
            return redirect('login')
    else:
        form = CommentForm()

    context = {
        'blog': blog,
        'comments': comments,
        'form': form
    }
    return render(request, 'user/blog_detail.html', context)




from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import InquiryForm

def submit_inquiry(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your inquiry has been submitted successfully. We will get back to you soon!')
            return redirect('submit_inquiry')  # Redirect to the same page after submission
    else:
        form = InquiryForm()
    
    return render(request, 'user/inquiry_form.html', {'form': form})

