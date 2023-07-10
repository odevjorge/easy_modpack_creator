from django.shortcuts import render, redirect
from django.urls import reverse

from api.classes import CurseForgeAPI


def config_view(request):
    if request.method == "GET":
        context = {
            'versions': CurseForgeAPI().return_game_versions(),
            'modloaders': CurseForgeAPI().return_mod_loaders()
        }
        return render(request, "config.html", context=context)

    elif request.method == "POST":
        url = reverse('search', args=('1.18.2', 'forge'))

        return redirect(url)


def search_mods_view(request, version, modloader):
    if request.GET.get('search'):
        search_mod = request.GET.get('search')

        api = CurseForgeAPI()

        pagination = 1
        if request.GET.get('page'):
            pagination = int(request.GET.get('page'))
        mods_list = api.search_mods_by_name(mod=search_mod, pagination=pagination).json()

        mods = []
        for c in mods_list['data']:
            mod_files = api.get_mod_files(c['id'])['data']

            mods.append({
                "mod_name": c['name'],
                "mod_icon": c['logo']['url'],
                "mod_author": c['authors'][0]['name'],
                "downloads": c['downloadCount'],
                "lasted_on_version_file": {
                    "game_version": api.GAME_VERSION,
                    "file_name": mod_files[0]['displayName'],
                    "download_url": mod_files[0]['downloadUrl'],
                },
                "others_files": mod_files
            })

        if mods_list['pagination']['totalCount'] <= mods_list['pagination']['pageSize']:
            end = 1
        else:
            end = (mods_list['pagination']['totalCount'] / mods_list['pagination']['pageSize']) + 1

        pagination = ''.join([str(num) for num in range(1, -int(-end // 1))])

        context = {
            'mods': mods,
            'pagination': pagination,
            'search_value': search_mod
        }

        return render(request, "homepage.html", context=context)

    elif request.method == 'GET':

        return render(request, "homepage.html", context=None)

"""
AS CONSULTAS ESTÃO DEMORANDO PARA RETORNAR RESULTADOS: GUARDAR O RETORNO DAS CONSULTAS NO BANCO
DE DADOS E FAZER A CONSULTA NO BANCO PODE SER UMA ALTERNATIVA. CASO A CONSULTA NÃO EXISTA PODE 
SER FEITA UMA CONSULTA NA E A RESPOSTA SER GUARDADA NO BANCO, QUANDO MUITOS USUARIOS ESTIVEREM 
USANDO A APLICAÇÃO A QUANTIDADE DE CONSULTAS NA API VAI SER MINIMA. 
"""