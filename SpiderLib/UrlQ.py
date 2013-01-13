#!/usr/bin/env python
#coding=utf-8

class UrlQ(object):
	def del_re(self):
		'''删掉重复的url'''
		return list(set(self.obj_href))
	def del_nosite(self):
		'''删掉无关的url'''
		pass
	def status(self):
		'''
		检查连接状态
		0：连接正常
		1：连接不成功
		'''
		pass
	def deep(self):
		'''检查连接深度，根目录深度为0，以后递增'''
		pass
