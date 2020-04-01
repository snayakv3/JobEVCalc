from django.shortcuts import render
from . import controller

def index(request):
    if(request.POST):
        team_data = request.POST.get('team')
        meta_data = request.META
        error_message, best_days, power_items, team_data = controller.calculate_job_ev_days(team_data, meta_data)
        context={
            'days' : best_days,
            'power_items':power_items,
            'error':error_message
        }
        if team_data is not None:
            context['user_input'] = team_data
        return render(request, 'EVCalc_app/index.html', context=context)
    else:
        return render(request, 'EVCalc_app/index.html')

def error_page(request):
    return render(request, 'EVCalc_app/error.html')
