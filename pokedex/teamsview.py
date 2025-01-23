import json
from django.contrib import messages
from django.shortcuts import render
from pokedex.models import Teams
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import requests
from pokedex.views import API_URL


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "PATCH", "DELETE"])
def manageTeam(request):

    if request.method in {'GET', 'POST'}:
        try:
            response = requests.get(f"{API_URL}?&limit=151")
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException:
            return HttpResponse("Pokémons not found", status=404)
        pokemons = data.get("results", [])

        teams = Teams.objects.all()
        for team in teams:
            team.pokemons = [team.pokemon_1,team.pokemon_2,team.pokemon_3,team.pokemon_4,team.pokemon_5,team.pokemon_6]
        
        all_pokemons = []
        for pokemon in pokemons:
            pokemon_url = pokemon['url']
            try:
                response_pokemon = requests.get(pokemon_url)
                response_pokemon.raise_for_status()
                data_pokemon = response_pokemon.json()
                name = data_pokemon['name']
                image_url = data_pokemon['sprites']['front_default']
                all_pokemons.append({
                    'id' : data_pokemon['id'],
                    'name': name,
                    'image_url': image_url,
                })
            except requests.exceptions.RequestException:
                continue  

    if request.method == 'GET':
        return render(request, 'teams.html', {'teams': teams, 'all_pokemons': all_pokemons})

    
    if request.method == 'POST':
        name = request.POST.get('name')
        pokemon_name_1 = request.POST.get('pokemon-name1')
        pokemon_name_2 = request.POST.get('pokemon-name2')
        pokemon_name_3 = request.POST.get('pokemon-name3')
        pokemon_name_4 = request.POST.get('pokemon-name4')
        pokemon_name_5 = request.POST.get('pokemon-name5')
        pokemon_name_6 = request.POST.get('pokemon-name6')
        if name:
            team = Teams.objects.create(
                name=name, 
                pokemon_1=pokemon_name_1,
                pokemon_2=pokemon_name_2,
                pokemon_3=pokemon_name_3,
                pokemon_4=pokemon_name_4,
                pokemon_5=pokemon_name_5,
                pokemon_6=pokemon_name_6,
                )
            # team = Teams(name=name)
            team.save()
            messages.success(request, f"Team '{name}' created successfully!")
            
            #add 6 pokemons to the team
            # team.pokemons.add(pokemon1, pokemon2, pokemon3)
            # team.save()
            
            #messages.success(request, f"List of pokemon added successfully!")
            
            return render(request, 'teams.html', {'teams': Teams.objects.all(), 'all_pokemons': all_pokemons})
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
            pokemon_1 = data.get('pokemon_1')
            pokemon_2 = data.get('pokemon_2')
            pokemon_3 = data.get('pokemon_3')
            pokemon_4 = data.get('pokemon_4')
            pokemon_5 = data.get('pokemon_5')
            pokemon_6 = data.get('pokemon_6')
            # print(f'team_id', team_id), print(f'new_name', new_name)

            if team_id and new_name:
                team = Teams.objects.get(id=team_id)
                team.name = new_name
                team.pokemon_1 = pokemon_1
                team.pokemon_2 = pokemon_2
                team.pokemon_3 = pokemon_3
                team.pokemon_4 = pokemon_4
                team.pokemon_5 = pokemon_5
                team.pokemon_6 = pokemon_6
                team.save()
                return JsonResponse({'message': f"Team '{team_id}' updated successfully!"}, status=200)
            else:
                return JsonResponse({'message': "Team ID and name are required."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': "Invalid JSON data."}, status=400)
        except Teams.DoesNotExist:
            return JsonResponse({'message': "Team not found."}, status=404)


    return HttpResponse(status=405)

@csrf_exempt
@require_http_methods(["POST"])
def battle(request):
    try:
        data = json.loads(request.body)
        team1_id = data.get('team1_id')
        team2_id = data.get('team2_id')

        if not team1_id or not team2_id:
            return JsonResponse({'message': "Both team IDs are required."}, status=400)

        team1 = Teams.objects.get(id=team1_id)
        team2 = Teams.objects.get(id=team2_id)

        def get_pokemon_hp(pokemon_name):
            if not pokemon_name:
                return 0
            response = requests.get(f"{API_URL}/{pokemon_name}")
            if response.status_code == 200:
                data = response.json()
                return data['stats'][0]['base_stat']
            return 0

        team1_hp = sum(get_pokemon_hp(pokemon) for pokemon in [team1.pokemon_1, team1.pokemon_2, team1.pokemon_3, team1.pokemon_4, team1.pokemon_5, team1.pokemon_6])
        team2_hp = sum(get_pokemon_hp(pokemon) for pokemon in [team2.pokemon_1, team2.pokemon_2, team2.pokemon_3, team2.pokemon_4, team2.pokemon_5, team2.pokemon_6])

        if team1_hp > team2_hp:
            winner = team1.name
        else:
            winner = team2.name

        return JsonResponse({'message': f"The winner is {winner}!"}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'message': "Invalid JSON data."}, status=400)
    except Teams.DoesNotExist:
        return JsonResponse({'message': "One or both teams not found."}, status=404)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def battle_page(request):
    if request.method == 'GET':
        teams = Teams.objects.all()
        return render(request, 'battle.html', {'teams': teams})

    if request.method == 'POST':
        data = json.loads(request.body)
        team1_id = data.get('team1_id')
        team2_id = data.get('team2_id')

        if not team1_id or not team2_id:
            return JsonResponse({'message': "Both team IDs are required."}, status=400)

        team1 = Teams.objects.get(id=team1_id)
        team2 = Teams.objects.get(id=team2_id)

        def get_pokemon_hp(pokemon_name):
            if not pokemon_name:
                return 0
            response = requests.get(f"{API_URL}/{pokemon_name}")
            if response.status_code == 200:
                data = response.json()
                return data['stats'][0]['base_stat']
            return 0

        team1_hp = sum(get_pokemon_hp(pokemon) for pokemon in [team1.pokemon_1, team1.pokemon_2, team1.pokemon_3, team1.pokemon_4, team1.pokemon_5, team1.pokemon_6])
        team2_hp = sum(get_pokemon_hp(pokemon) for pokemon in [team2.pokemon_1, team2.pokemon_2, team2.pokemon_3, team2.pokemon_4, team2.pokemon_5, team2.pokemon_6])

        if team1_hp > team2_hp:
            winner = team1.name
        else:
            winner = team2.name

        return JsonResponse({'message': f"The winner is {winner}!"}, status=200)
