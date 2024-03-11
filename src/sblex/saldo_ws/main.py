from sblex.saldo_ws import config, server

settings = config.read_settings_from_env()
print(f"{settings=}")

app = server.create_saldo_ws_server(settings=settings)
