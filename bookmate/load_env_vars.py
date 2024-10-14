from dotenv import load_dotenv
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(current_dir, "../"))
templates_dir = os.path.join(base_dir, "templates")
admin_templates_dir = os.path.join(templates_dir, "admin")

# Load environment variables from .env file
load_dotenv()

class VarSettings():
    ISBN_API_KEY: str = os.getenv("ISBN_API_KEY", "")
    FREE_RENTAL_PERIOD: int = int(os.getenv("FREE_RENTAL_PERIOD", 30))
    admin_templates_dir: str = admin_templates_dir
    templates_dir: str = templates_dir

var_settings = VarSettings()