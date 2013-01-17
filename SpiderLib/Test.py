#coding:utf-8
#Python���̳߳�ʵ��

import Queue
import threading
import sys
import time
import urllib

#�����ǹ������̳߳��е��߳�
class MyThread(threading.Thread):
	def __init__(self, workQueue, resultQueue,timeout=30, **kwargs):
		threading.Thread.__init__(self, kwargs=kwargs)
	#�߳��ڽ���ǰ�ȴ�������ж೤ʱ��
		self.timeout = timeout
		self.setDaemon(True)
		self.workQueue = workQueue
		self.resultQueue = resultQueue
		self.start()

	def run(self):
		while True:
			try:
				#�ӹ��������л�ȡһ������
				callable, args, kwargs = self.workQueue.get(timeout=self.timeout)
				#����Ҫִ�е�����
				res = callable(args, kwargs)
				#�����񷵻صĽ�����ڽ��������
				self.resultQueue.put(res+" | "+self.getName())    
			except Queue.Empty: #������пյ�ʱ��������߳�
				break
			except :
				print sys.exc_info()
				raise

class ThreadPool:
	def __init__( self, num_of_threads=10):
		self.workQueue = Queue.Queue()
		self.resultQueue = Queue.Queue()
		self.threads = []
		self.__createThreadPool( num_of_threads )

	def __createThreadPool( self, num_of_threads ):
		for i in range( num_of_threads ):
			thread = MyThread( self.workQueue, self.resultQueue )
			self.threads.append(thread)

	def wait_for_complete(self):
		#�ȴ������߳���ɡ�
		while len(self.threads):
			thread = self.threads.pop()
			#�ȴ��߳̽���
			if thread.isAlive():#�ж��߳��Ƿ񻹴���������Ƿ����join
				thread.join()

	def add_job( self, callable, *args, **kwargs ):
		self.workQueue.put( (callable,args,kwargs) )

def test_job(id, sleep = 0.001 ):
	html = ""
	try:
		time.sleep(1)
		conn = urllib.urlopen('http://www.google.com/')
		html = conn.read(20)
	except:
		print  sys.exc_info()
	return  html

def test():
	print 'start testing'
	tp = ThreadPool(3)
	for i in range(10):
		time.sleep(0.2)
		tp.add_job( test_job, i, i*0.001 )
	tp.wait_for_complete()
	#������
	print 'result Queue\'s length == %d '% tp.resultQueue.qsize()
	while tp.resultQueue.qsize():
		print tp.resultQueue.get()
	print 'end testing'

def testA():
	from urllib2 import Request, urlopen, URLError, HTTPError
	import urllib2
	req = urllib2.Request('http://www.pretend_server.org')
	try: urllib2.urlopen(req)
	except URLError, e:
		print str(e.reason)+"\n"+str(e.code)

import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# Never do this -- insecure!
symbol = 'RHAT'
c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

# Do this instead
t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)

# Larger example that inserts many records at a time
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
conn.commit()
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
#print c.fetchone()
#print c.fetchall()
import pdb
pdb.set_trace()

