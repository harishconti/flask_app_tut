from dotenv import load_dotenv
import os
load_dotenv('db_auth.env')
print(os.getenv('instance_connection_name'))