from django.conf import settings
from smart.models import *
from string import Template
import re
import sys
import os
from django.utils import simplejson
import urllib2


def sub(str, var, val):
    return str.replace("{%s}"%var, val)


def LoadApp(app):
    # Some basic apps and a couple of accounts to get things going.
  print app
  if not app.startswith("http"):
      s = open(app)
      base_url="unknown"
  else:
      base_url = re.search("https?://.*?[/$]", app).group()[:-1]
      s = urllib2.urlopen(app)

  r = simplejson.loads(s.read())

  if ('base_url' not in locals()):
    base_url = r["base_url"]
  
  if r["mode"] == "background" or r["mode"] == "helper":
      a = HelperApp.objects.create(
                       description = r["description"],
                       consumer_key = r["id"],
                       secret = 'smartapp-secret',
                       name =r["name"],
                       email=r["id"])
      
  elif r["mode"] == "ui":
      exists = PHA.objects.filter(email=r["id"])
      assert len(exists) <2, "Found >1 PHA by the name %s"%r["id"]
      if len(exists)==1:
          print exists[0]
          print "deleting, exists."
          exists[0].delete()

      a = PHA.objects.create(
                       description = r["description"],
                       consumer_key = r["id"],
                       secret = 'smartapp-secret',
                       name =r["name"],
                       email=r["id"],
                       icon_url=sub(r["icon"], "base_url", base_url),
                       enabled_by_default=False)
  else: a = None

  try:
    for (act_name, act_url) in r["activities"].iteritems():
      act_url = sub(act_url, "base_url", base_url)
      AppActivity.objects.create(app=a, name=act_name, url=act_url)
  except: pass

  try:
    for (hook_name, hook_data) in r["web_hooks"].iteritems():
      hook_url = sub(hook_data["url"], "base_url", base_url)

      try: rpc = hook_data['requires_patient_context']
      except: rpc = False
      
      AppWebHook.objects.create(app=a,
                              name=hook_name, 
                              description=hook_data["description"],
                              url=hook_url,
                              requires_patient_context=rpc)
  except: pass
  print "done ", app
  s.close() 

if __name__ == "__main__":
    import string
    for v in sys.argv[1:]:
        print "Loading app: %s"%v
        LoadApp(v)

