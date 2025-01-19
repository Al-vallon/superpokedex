import json
from django.contrib import messages
from django.shortcuts import render
from pokedex.models.teams import Teams
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "PATCH", "DELETE"])
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

    if request.method == 'DELETE':
        try:
            data = json.loads(request.body) 
            team_id = data.get('id')
            if team_id:
                team = Teams.objects.get(id=team_id)
                team_name = team.name
                team.delete()
                messages.success(request, f"Team '{team_name}' deleted successfully!")
                return JsonResponse({'message': f"Team '{team_name}' deleted successfully!"}, status=204)
            else:
                return JsonResponse({'message': "Team ID is required."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': "Invalid JSON data."}, status=400)
        except Teams.DoesNotExist:
            return JsonResponse({'message': "Team not found."}, status=404)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            team_id = data.get('team_id')
            new_name = data.get('name')
            # print(f'team_id', team_id), print(f'new_name', new_name)

            if team_id and new_name:
                team = Teams.objects.get(id=team_id)
                team.name = new_name
                team.save()
                return JsonResponse({'message': f"Team '{team_id}' updated to '{new_name}' successfully!"}, status=200)
            else:
                return JsonResponse({'message': "Team ID and new name are required."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': "Invalid JSON data."}, status=400)
        except Teams.DoesNotExist:
            return JsonResponse({'message': "Team not found."}, status=404)


    return HttpResponse(status=405)
