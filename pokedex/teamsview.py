from django.contrib import messages
from django.shortcuts import render
from pokedex.models.teams import Teams
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse


# def teams(request):
#     teams_list = Teams.objects.get.all()
#     context = {'teams': teams_list}
#     return render(request, 'teams.html', context)

@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def manageTeam(request):
    if request.method == 'GET':
        teams = Teams.objects.all()
        return render(request, 'teams.html', {'teams': teams})
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            team = Teams.objects.create(name=name)
            # team = Teams(name=name)
            team.save()
            messages.success(request, f"Team '{name}' created successfully!")
            
            #add 6 pokemons to the team
            # team.pokemons.add(pokemon1, pokemon2, pokemon3)
            # team.save()
            
            #messages.success(request, f"List of pokemon added successfully!")
            
            return render(request, 'teams.html', {'teams': Teams.objects.all()})
        else:
            messages.error(request, "Team could not be created. Name is required.")
            return render(request, 'teams.html')  

    return HttpResponse(status=405)