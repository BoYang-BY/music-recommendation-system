from utils import hdf5_getters


def extract_h5_info(h5, i=0):
    return {
        "artist_hotness": float(hdf5_getters.get_artist_hotttnesss(h5, i)),
        "artist_id": hdf5_getters.get_artist_id(h5, i).decode("utf-8"),
        "artist_name": hdf5_getters.get_artist_name(h5, i).decode("utf-8"),

        "artist_terms": [
            term.decode("utf-8")
            for term in hdf5_getters.get_artist_terms(h5, i)
        ],

        "artist_terms_freq":
            hdf5_getters.get_artist_terms_freq(h5, i).tolist(),

        "artist_terms_weight":
            hdf5_getters.get_artist_terms_weight(h5, i).tolist(),

        "song_id":
            hdf5_getters.get_song_id(h5, i).decode("utf-8"),

        "song_hotness":
            float(hdf5_getters.get_song_hotttnesss(h5, i)),

        "song_title":
            hdf5_getters.get_title(h5, i).decode("utf-8"),

        "audio_features": {
            "danceability":
                float(hdf5_getters.get_danceability(h5, i)),

            "energy":
                float(hdf5_getters.get_energy(h5, i)),

            "key":
                int(hdf5_getters.get_key(h5, i)),

            "loudness":
                float(hdf5_getters.get_loudness(h5, i)),

            "tempo":
                float(hdf5_getters.get_tempo(h5, i)),
        },

        "year":
            int(hdf5_getters.get_year(h5, i))
    }