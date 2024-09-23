import os


class Config:
    DEBUG = os.getenv("DEBUG")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_PORT")

    LLM_CONFIG = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant that helps people find information. If you cannot find the information you've been asked for, you can ask the person to write a question more clearly or provide more context.",
                    }
                ],
            }
        ],
        "temperature": 0.2,
        "top_p": 0.95,
        "max_tokens": 800,
        "model": "gpt-4o",
    }


class NetflixConfig(Config):

    def __init__(self):
        self.logo = "https://upload.wikimedia.org/wikipedia/commons/e/e6/N-iX_logo.jpg"
        self.title = "Netflix Assistant"
        self.subtitle = "Ask questions about Netflix's movies and shows."

    def get_logo(self):
        return self.logo

    def get_title(self):
        return self.title

    def get_subtitle(self):
        return self.subtitle

    @staticmethod
    def load_training_data(vn):
        from text2sql.src.train.netflix import load_training_data

        return load_training_data(vn)


class FirstStudentConfig(Config):

    def __init__(self):
        self.logo = "https://firststudentinc.com/wp-content/uploads/FirstStudentLogo_FC_notag.svg"
        self.title = "Reporting Assistant"
        self.subtitle = "Generative AI-powered solution for extracting routes and contracts data."

    def get_logo(self):
        return self.logo

    def get_title(self):
        return self.title

    def get_subtitle(self):
        return self.subtitle

    @staticmethod
    def load_training_data(vn):
        from text2sql.src.train.fs import load_training_data

        return load_training_data(vn)
