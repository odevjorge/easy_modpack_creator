import re

from flask import Flask, render_template, request

from core.ForgeAPIRequests import ForgeAPIRequests

app = Flask(__name__)

mod_loaders = {
    0: "Any",
    1: "Forge",
    2: "Cauldron",
    3: "LiteLoader",
    4: "Fabric",
    5: "Quilt"
}


@app.route('/')
def home():
    json_requests = ForgeAPIRequests()

    versions = json_requests.request(url='/minecraft/version').json()['data']

    context = {
        'versions': versions,
        'modloaders': mod_loaders
    }

    return render_template("config.html", context=context)


@app.route('/<version>/<mod_loader>/<mod>', methods=['GET'])
@app.route('/<version>/<mod_loader>', methods=['GET', 'POST'])
def search_mods(version, mod_loader, mod_name=None):
    if request.args.get('search'):
        search_mod = request.args.get('search')

        api = ForgeAPIRequests()
        if re.match(r"^(?:\d{1,2}\.){2}\d{1,2}$", version):
            api.switch_game_version(version)
        else:
            msg = "Error: padrão de versão não compativel, recarrege a pagina e tente novamente"
            return render_template("error.html", error=msg)

        if mod_loader in mod_loaders.values():
            api.switch_mod_loader(mod_loader.upper())
        else:
            msg = "Error: mod loader não compativel com o esperado, recarrege a pagina e tente novamente"
            return render_template("error.html", error=msg)

        pagination = 1
        if request.args.get('pagination'):
            pagination = int(request.args.get('pagination'))
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

        return render_template("homepage.html", mods=mods, pagination=pagination, search_value=search_mod)

    elif request.method == 'GET':

        return render_template("homepage.html", context=None)


if __name__ == '__main__':
    app.run(debug=True)
