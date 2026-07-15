# telemetry/assets.py

TRACK_IMAGES = {
    "spa": "img/tracks/spa.png",
    "monza": "img/tracks/monza.png",
    "imola": "img/tracks/imola.png",
    "interlagos": "img/tracks/interlagos.png",
    "brasil": "img/tracks/interlagos.png",
    "silverstone": "img/tracks/silverstone.png",
    "laguna": "img/tracks/laguna.png",
    "laguna seca": "img/tracks/laguna.png",
    "mugello": "img/tracks/mugello.png",
    "nurburgring": "img/tracks/nurburgring.png",
    "nürburgring": "img/tracks/nurburgring.png",
    "hungaroring": "img/tracks/hungaroring.png",
    "monaco": "img/tracks/monaco.png",
    "monte carlo": "img/tracks/monaco.png",
    "suzuka": "img/tracks/suzuca.png",
    "suzuca": "img/tracks/suzuca.png",
    "yokohama": "img/tracks/suzuca.png",
    "japao": "img/tracks/suzuca.png",     # caso venha escrito assim
    "bahrain": "img/tracks/barain.png",
    "barain": "img/tracks/barain.png",
    "ardennes": "img/tracks/ardenas.png",
    "rio de janeiro": "img/tracks/rio de janeiro.png",
    "guildford": "img/tracks/guildford.png",
    "milan": "img/tracks/milao.png",
}


CAR_IMAGES = {
    "458_gt2": "img/cars/458gt2.png",
    "458gt2": "img/cars/458gt2.png",

    "m3_gt2": "img/cars/M3gt2.png",
    "m3gt2": "img/cars/M3gt2.png",

    "z4_gt3": "img/cars/Z4gt3.png",
    "z4gt3": "img/cars/Z4gt3.png",

    "amg_gt3": "img/cars/amggt3.png",
    "amggt3": "img/cars/amggt3.png",

    "mp4-12c": "img/cars/MP4-4gt3.png",
    "mp4": "img/cars/MP4-4gt3.png",

    "lotus": "img/cars/lotus.png",

    "force india": "img/cars/forceindia.png",
    "forceindia": "img/cars/forceindia.png",

    "ferrari": "img/cars/ferrari.png",

    "caterham": "img/cars/catheran.png",
    "catheran": "img/cars/catheran.png",

    "mercedes": "img/cars/mercedez.png",
    "mercedez": "img/cars/mercedez.png",

    "mclaren": "img/cars/mclaren.png",

    "marussia": "img/cars/marrusia.png",
    "marrusia": "img/cars/marrusia.png",

    "williams": "img/cars/wilians.png",
    "wilians": "img/cars/wilians.png",

    "toro rosso": "img/cars/tororosso.png",
    "tororosso": "img/cars/tororosso.png",

    "sauber": "img/cars/sauber.png",

    "red bull": "img/cars/redbull.png",
    "redbull": "img/cars/redbull.png",

    "steinmann": "img/cars/steinmann.png",
    "rossini": "img/cars/rossini.png",
    "panther": "img/cars/panther.png",
    "windsor": "img/cars/windsor.png",
    "kitano": "img/cars/kitano.png",
    "rezzato": "img/cars/rezzato.png",
    "chariot": "img/cars/chariot.png",
    "macneil": "img/cars/macneil.png",
    "mersault": "img/cars/mersault.png",
}


from django.templatetags.static import static


def get_track_image(track):

    if not track:
        return static("img/tracks/default.png")

    track = track.lower()

    for key, image in TRACK_IMAGES.items():
        if key in track:
            return static(image)

    return static("img/tracks/default.png")


def get_car_image(car):

    if not car:
        return static("img/cars/default.png")

    car = car.lower()

    for key, image in CAR_IMAGES.items():
        if key in car:
            return static(image)

    return static("img/cars/default.png")