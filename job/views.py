# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
import os
import sys
import subprocess
import bug_oracle
from django.http import HttpResponse
import json	

# Create your views here.

class RunScript(View):

	template_name = 'job/jenkin.html'	
	def get(self, request):

		try:

			return render(request, self.template_name, {})
			
		except Exception as e:
			print e, "Exception"

	def post(self, request):

		try:
			key = request.POST.get("jen")
			tested = bug_oracle.bugOracle(key)
			print tested, "{{{{{{{{{{{"
			response = {
				"text": tested
			}
			print response, "???????????????"
			return HttpResponse(json.dumps(response), content_type="application/json")
		except Exception as e:
			print e, "Exception"