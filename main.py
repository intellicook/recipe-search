import logging

from configs import logging as logging_configs

logging.basicConfig(level=logging_configs.configs.logging_level)


if __name__ == "__main__":
    from apis import server

    server.start()
