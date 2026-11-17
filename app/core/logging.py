import logging


def setup_logging():

    logging.basicConfig(
        level=logging.DEBUG if __import__("os").getenv(
            "DEBUG", "False"
        ).lower() == "true" else logging.INFO,

        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        )
    )


logger = logging.getLogger("fastapiprojectdb")