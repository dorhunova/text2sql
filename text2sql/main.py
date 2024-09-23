import os
import logging

from dotenv import load_dotenv
from openai import AzureOpenAI
from vanna.chromadb import ChromaDB_VectorStore
from vanna.flask import VannaFlaskApp
from vanna.openai import OpenAI_Chat

from text2sql.src.utils import strtobool

load_dotenv()


class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):

    def __init__(self, config=None):
        self.client = self.init_azure_client()
        ChromaDB_VectorStore.__init__(self, config=config.LLM_CONFIG)
        OpenAI_Chat.__init__(self, client=self.client, config=config.LLM_CONFIG)

    def init_azure_client(self):
        api_base = os.getenv("API_BASE")
        api_version = os.getenv("API_VERSION")
        api_key = os.getenv("API_KEY")
        deployment = os.getenv("DEPLOYMENT")

        client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=api_base,
            azure_deployment=deployment,
            api_key=api_key,
        )
        return client


if __name__ == "__main__":

    client = os.getenv("CLIENT")

    if client == "fs":
        from text2sql.src.config import FirstStudentConfig

        config = FirstStudentConfig()
    elif client == "netflix":
        from text2sql.src.config import NetflixConfig

        config = NetflixConfig()
    else:
        raise ValueError(f"Invalid client: {client}")

    vn = MyVanna(config=config)

    vn.connect_to_postgres(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )

    # Remove old training records for clean demo
    for id in vn.get_training_data().id.values:
        vn.remove_training_data(str(id))

    config.load_training_data(vn)
    logging.info(f"{type(config.logo)}")
    app = VannaFlaskApp(
        vn,
        allow_llm_to_see_data=bool(
            strtobool(os.getenv("ALLOW_LLM_TO_SEE_DATA", "False"))
        ),
        debug=bool(strtobool(os.getenv("DEBUG", "False"))),
        sql=bool(strtobool(os.getenv("SQL", "False"))),
        chart=bool(strtobool(os.getenv("CHART", "False"))),
        redraw_chart=bool(strtobool(os.getenv("REDRAW_CHART", "False"))),
        logo=config.get_logo(),
        title=config.get_title(),
        subtitle=config.get_subtitle(),
        summarization=bool(strtobool(os.getenv("SUMMARIZATION", "False"))),
    )

    app.run()
