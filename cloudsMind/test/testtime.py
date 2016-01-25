
# import datetime
#
# t=datetime.datetime.time('2015-12-28 15:34:18.135665311')
# print t

str='recv(281000): total=8225, rate=1470(msg/sec)'

line=str.split(',')[-1].split('=')[-1].split('(')[0]

print line