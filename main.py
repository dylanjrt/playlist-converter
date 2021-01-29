from glue import Glue


def run():

    yt_json_source = "./creds/client_secret.json"
    sp_creds_source = "./creds/secrets2.txt"

    initializer = Glue(yt_json_source, sp_creds_source)
    initializer.generate("Summer Mix 2017")


if __name__ == '__main__':
    run()
