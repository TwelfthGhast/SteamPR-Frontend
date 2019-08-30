from flask import Flask, render_template, redirect, request
from flask_caching import Cache
import requests
import time
import config as cfg
import locale #comma formatting for numbers

cacheconfig = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 60*60*12
}

app = Flask(__name__)
app.config.from_mapping(cacheconfig)
cache = Cache(app)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

APIKEY = cfg.apikey
APIURL = cfg.apiurl

STATUS_PERMANENTLY_MOVED = 302
STATUS_NOT_FOUND = 404

ERROR_404_COULD_NOT_RESOLVE = 0
ERROR_404_NOT_IN_DB = 1
ERROR_404_NOT_FOUND = 2

def calc_xp(level):
    xp = 0
    max = int(int(level) / 10)
    for i in range(max + 1):
        xp += i * 10
    xp = xp * 100
    for i in range(max * 10, int(level)):
        xp += (max + 1) * 100
    return int(xp)


def calc_lvl(xp):
    multi = 1
    level = 0
    while (xp - multi * 1000) >= 0:
        xp -= multi * 1000
        multi += 1
        level += 10
    while xp - multi * 100 >= 0:
        xp -= multi * 100
        level += 1
    return int(level)


def epoch_readable(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))


@app.route('/api/')
def redirect_api():
    return redirect("https://api.steampagerank.com/", code=STATUS_PERMANENTLY_MOVED)

@app.route('/12ghast/')
def redirect_12ghast():
    return redirect("https://www.12ghast.com/", code=STATUS_PERMANENTLY_MOVED)

@app.route('/')
@cache.memoize(timeout=60*60*24*7)
def main_page():
    num_track = requests.get(APIURL + "GetCount/")
    data_num = num_track.json()
    return render_template('index.html', in_accno=locale.format("%d", data_num['count'], grouping=True))


@app.errorhandler(404)
def redirect_404(error):
    return redirect("/notfound", code=STATUS_PERMANENTLY_MOVED)

@app.route('/notfound/')
@cache.memoize(timeout=60*60*24*7)
def render_404():
    return render_template('404.html', error404=ERROR_404_NOT_FOUND)

@app.route('/ladder/')
@cache.memoize(timeout=60*60*24*7)
def ladder_page():
    parameters = {"limit": 200, "lvlmin": 50}
    rank_json = requests.get(APIURL + "GetList/", parameters)
    data_json = rank_json.json()
    return render_template('ladder.html', in_rank=data_json)


def render_user(data_badges, parameters_steam, steamid64, data_friends):
    account = requests.get("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/",
                           params=parameters_steam)
    data_acc = account.json()
    app.logger.info('%s', data_acc)
    cur_epoch = time.time()

    epochcount = cur_epoch
    xpcount = 0
    if "badges" in data_badges:
        for data_badge in data_badges['badges']:
            xpcount += data_badge['xp']
        chart_data = "[ 0, " + str(calc_lvl(xpcount)) + ", \"" + \
                     data_acc['response']['players'][0]['personaname'] + \
                     " was level " + str(calc_lvl(xpcount)) + " at " + time.strftime('%m/%Y',
                                                                                     time.localtime(epochcount)) + "\"]"
        monthcount = 0
        for data_badge in data_badges['badges']:
            if data_badge['completion_time'] <= epochcount + int(60 * 60 * 24 * 30.4375):
                chart_data += ", [" + str(monthcount) + ", " + str(calc_lvl(xpcount)) + ", \"" + \
                              data_acc['response']['players'][0]['personaname'] + \
                              " was level " + str(calc_lvl(xpcount)) + " at " + time.strftime('%m/%Y', time.localtime(
                    epochcount)) + "\"]"
                epochcount -= int(60 * 60 * 24 * 30.4375)
                monthcount -= 1
                while data_badge['completion_time'] <= epochcount + int(60 * 60 * 24 * 30.4375):
                    chart_data += ", [" + str(monthcount) + ", " + str(calc_lvl(xpcount)) + ", \"" + \
                                  data_acc['response']['players'][0]['personaname'] + \
                                  " was level " + str(calc_lvl(xpcount)) + " at " + time.strftime('%m/%Y', time.localtime(
                        epochcount)) + "\"]"
                    monthcount -= 1
                    epochcount -= int(60 * 60 * 24 * 30.4375)
            xpcount -= data_badge['xp']
        chart_data += ", [" + str(monthcount) + ", " + str(calc_lvl(xpcount)) + ", \"" + \
                      data_acc['response']['players'][0]['personaname'] + \
                      " was level " + str(calc_lvl(xpcount)) + " at " + time.strftime('%m/%Y', time.localtime(epochcount)) + "\"]"
    else:
        chart_data = "[0, 0, \"" + data_acc['response']['players'][0]['personaname'] + " has a private profile.\"]"
    if 'timecreated' in data_acc['response']['players'][0]:
        account_age = int(
            (cur_epoch - data_acc['response']['players'][0]['timecreated']) * 100 / (60 * 60 * 24 * 365.25))
        account_age = account_age / 100
    else:
        account_age = 0
    ranking = requests.get(APIURL + "GetRank/" + str(steamid64))
    data_ranking = ranking.json()
    return render_template('user.html', in_badges=data_badges, in_account=data_acc, in_age=account_age,
                           in_rank=data_ranking, in_chart=chart_data, in_friends=data_friends)


@app.route('/profiles/<steamid64>')
# Cache results for 12 hours
@cache.memoize(timeout=60*60*12)
def generate_profile(steamid64):
    try:
        steamid64 = int(steamid64)
        parameters_internal = {"steamid": steamid64}
        parameters_steam = {"key": APIKEY, "steamids": steamid64, "steamid": steamid64}
        profile_json = requests.get(APIURL + "GetProfile/", params=parameters_internal)
        data_profile = profile_json.json()
        # If not in database
        if "error" in data_profile:
            crawl_badges = requests.get("https://api.steampowered.com/IPlayerService/GetBadges/v1/", params=parameters_steam)
            data_badges = crawl_badges.json()
            crawl_friends = requests.get("https://api.steampowered.com/ISteamUser/GetFriendList/v1/", params=parameters_steam)
            data_friends = crawl_friends.json()
            if "friendslist" in data_friends:
                return render_user(data_badges['response'], parameters_steam, steamid64, data_friends['friendslist'])
            else:
                return render_user(data_badges, parameters_steam, steamid64, data_friends)
        # If in database
        else:
            return render_user(data_profile, parameters_steam, steamid64, data_profile)
    except ValueError:
        return render_template('404.html', error404=ERROR_404_COULD_NOT_RESOLVE), STATUS_NOT_FOUND


@app.route('/search/')
def int_and_redirect():
    steamid64 = request.args.get("steamid64")
    try:
        steamid64=int(steamid64)
        if len(str(steamid64)) == 17 and steamid64 // 10000000000 == 7656119:
            return redirect("/profiles/" + str(steamid64), code=STATUS_PERMANENTLY_MOVED)
        else:
            raise ValueError()
    except ValueError:
        parameters = {"key": APIKEY, "vanityurl": steamid64}
        vanity = requests.get("https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/", params=parameters)
        data_vanity = vanity.json()
        if data_vanity['response']['success'] == 1:
            return redirect("/profiles/" + data_vanity['response']['steamid'], code=STATUS_PERMANENTLY_MOVED)
        else:
            return redirect("/profiles/" + str(steamid64), code=STATUS_PERMANENTLY_MOVED)


app.jinja_env.filters['convertepoch'] = epoch_readable

if __name__ == '__main__':
    app.run()
