import redis

r=redis.Redis(host='54.223.83.133',port=6379,db=0)
# info=r.info()
# print info
# r = redis.StrictRedis(host='54.223.83.133', port=6379, db=0)
length=r.llen('CPS.QUEUE.ANDROID')
print length