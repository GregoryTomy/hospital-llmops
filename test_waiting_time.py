import dotenv

dotenv.load_dotenv()

from chatbot.src.tools.wait_times import (get_current_wait_times,
                                          get_shortest_wait_hospital)

print(get_current_wait_times("Wallace-Hamilton"))
print(get_current_wait_times("not in database"))
print(get_shortest_wait_hospital(None))