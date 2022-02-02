from re import L
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from common.decorators import ajax_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.decorators.http import require_POST

# is ajax has been deprecated so I will create my own
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# Create your views here.
@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            messages.success(request,'Image added successfully')

            # redirect to the created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html',
                                {'section': 'images',
                                'form': form})

def image_detail(request,id,slug):
    image = get_object_or_404(Image,id=id,slug=slug)
    return render(request,'images/image/detail.html',{
                                            'section':'images',
                                            'image':image})

@login_required
@require_POST
@ajax_required
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    # result per page
    paginator = Paginator(images,8)
    # what page is the request asking for
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # if not page was passed to the request return first page
        images = paginator.page(1)
    except EmptyPage:
        if is_ajax(request):
            # if ajax and theres nothing on next page:
            return HttpResponse('')
        # if its normal request
        images = paginator.page(paginator.num_pages)
    if is_ajax(request):
        return render(request,'images/image/list_ajax.html',
                                {'section':'images',
                                'images':images})
    return render(request,'images/image/list.html',
                                {'section':'images',
                                'images':images})
