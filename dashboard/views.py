from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core.models import Contact
from django.utils.timezone import now
from django.core.paginator import Paginator

@login_required
def dashboard_home(request):
    search_query = request.GET.get('search')

    contacts = Contact.objects.all().order_by('-created_at')

    if search_query:
        contacts = contacts.filter(name__icontains=search_query)

    paginator = Paginator(contacts, 5)  # 5 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_contacts = Contact.objects.count()
    today_contacts = Contact.objects.filter(created_at__date=now().date()).count()

    context = {
        'page_obj': page_obj,
        'total_contacts': total_contacts,
        'today_contacts': today_contacts,
        'search_query': search_query,
    }

    return render(request, 'dashboard/home.html', context)



@login_required
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return redirect('dashboard_home')