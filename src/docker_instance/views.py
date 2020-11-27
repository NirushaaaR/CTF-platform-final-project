from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@staff_member_required
def create_instance(request):
    return render(request, "docker/create_instance.html")

@staff_member_required
def save_instance(request):
    docker_url = request.POST.get("docker")
    port = request.POST.get("port")
    is_deployed = request.POST.get("is_deployed")
    
    return