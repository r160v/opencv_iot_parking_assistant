import time
import datetime
import redis

r = redis.Redis()
r.mset({"Croatia": "Zagreb", "Bahamas": 1})
print(r.get("Bahamas"))
test = int(r.get("Bahamas"))
test += 1

r.set("Bahamas", test)
print(r.get("Bahamas"))


