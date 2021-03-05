from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def feedback_view(request):
    """ Get Feedback From User """
    return render(request, "core/feedback.html")