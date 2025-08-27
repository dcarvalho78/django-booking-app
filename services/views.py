# services/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Service

def service_list(request):
    q = (request.GET.get("q") or "").strip()
    qs = Service.objects.all()
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(category__icontains=q) |
            Q(description__icontains=q)
        )
    qs = qs.order_by("name")

    paginator = Paginator(qs, 10)  # 10 per page
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "services/service_list.html",
        {"page_obj": page_obj, "q": q},
    )

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, "services/service_detail.html", {"service": service})
