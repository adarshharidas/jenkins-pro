# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
import os
import sys
import subprocess
import test

# Create your views here.

class RunScript(View):


	def get(self, request):

		try:
			print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
			# os.system("python test.py")
			s2_out = subprocess.check_output([sys.executable, "test.py"])
			print s2_out, ":::::::::::::::::::::"
		except Exception as e:
			print e, "Exception"