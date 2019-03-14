from django.shortcuts import render, get_object_or_404, redirect
from .models import Posting, Comment


# Create your views here.
def posting_list(request):
    postings = Posting.objects.order_by('-updated_at')
    context = {}
    context['postings'] = postings

    return render(request, 'sns/list.html', context=context)


def posting_detail(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    comments = posting.comment_set.order_by('-created_at')
    context = {}
    context['posting'] = posting
    context['comments'] = comments

    return render(request, 'sns/detail.html', context=context)


def create_posting(request):
    if request.method == "POST":
        posting = Posting.objects.create(
            content=request.POST.get('content'),
            icon=request.POST.get('icon'),
            image=request.FILES.get('image'),
        )

        return redirect('sns:posting_detail', posting.id)

    else:
        return redirect('sns:posting_list')


def create_comment(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)

    if request.method == 'POST':
        content = request.POST.get('comment')
        comment = Comment()
        comment.content = content
        comment.posting = posting
        comment.save()

    return redirect('sns:posting_detail', posting.id)
