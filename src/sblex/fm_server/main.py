from sblex.fm_server import config, server

settings = config.read_settings_from_env()
print(f"{settings=}")

app = server.create_fm_server(settings=settings)
