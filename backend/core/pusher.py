from pathlib import Path
import pusher
import environ
import os

# Reading .env
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

PUSHER_SECRET = env('PUSHER_SECRET')
PUSHER_APP_ID = env('PUSHER_APP_ID')
PUSHER_KEY = env('PUSHER_KEY')
PUSHER_CLUSTER = env('PUSHER_CLUSTER')

pusher_client = pusher.Pusher(
  app_id=PUSHER_APP_ID,
  key=PUSHER_KEY,
  secret=PUSHER_SECRET,
  cluster=PUSHER_CLUSTER,
  ssl=True
)
