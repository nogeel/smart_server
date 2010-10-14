from django.conf import settings
from bootstrap_utils import interpolated_postgres_load, put_rdf
from smart.models import *
import os, glob

sample_dir = settings.APP_HOME#os.path.join(settings.APP_HOME, "bootstrap_helperes/sample_data")
sample_patients = [os.path.split(x)[-1] for x in glob.glob("%s/records/*"%sample_dir)]

for s in sample_patients:
    Record.objects.create(id=s)


bios = []
bios.append("""
<rdf:Description rdf:about="http://smartplatforms.org/records/%s">
  <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
  <foaf:familyName>Bach</foaf:familyName>
  <foaf:givenName>Hiram</foaf:givenName>
  <foaf:gender>male</foaf:gender>
  <spdemo:zipcode>02543</spdemo:zipcode>
  <spdemo:birthday>19631215</spdemo:birthday>
</rdf:Description>
""")
bios.append("""
<rdf:Description rdf:about="http://smartplatforms.org/records/%s">
  <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
  <foaf:familyName>Schnur</foaf:familyName>
  <foaf:givenName>Bert</foaf:givenName>
  <foaf:gender>male</foaf:gender>
  <spdemo:zipcode>63050</spdemo:zipcode>
  <spdemo:birthday>19450419</spdemo:birthday>
</rdf:Description>
""")
bios.append("""
<rdf:Description rdf:about="http://smartplatforms.org/records/%s">
  <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
  <foaf:familyName>Paltrow</foaf:familyName>
  <foaf:givenName>Bruce</foaf:givenName>
  <foaf:gender>male</foaf:gender>
  <spdemo:zipcode>54360</spdemo:zipcode>
  <spdemo:birthday>19450201</spdemo:birthday>
</rdf:Description>
""")
bios.append("""
<rdf:Description rdf:about="http://smartplatforms.org/records/%s">
  <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
  <foaf:familyName>Cross</foaf:familyName>
  <foaf:givenName>David</foaf:givenName>
  <foaf:gender>male</foaf:gender>
  <spdemo:zipcode>08608</spdemo:zipcode>
  <spdemo:birthday>19720910</spdemo:birthday>
</rdf:Description>
""")
bios.append("""
<rdf:Description rdf:about="http://smartplatforms.org/records/%s">
  <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
  <foaf:familyName>Bergermeister</foaf:familyName>
  <foaf:givenName>Hans</foaf:givenName>
  <foaf:gender>male</foaf:gender>
  <spdemo:zipcode>19013</spdemo:zipcode>
  <spdemo:birthday>19631201</spdemo:birthday>
</rdf:Description>
""")
bios.append("""
<rdf:Description rdf:about="http://smartplatforms.org/records/%s">
  <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
  <foaf:familyName>Paltrow</foaf:familyName>
  <foaf:givenName>Mary</foaf:givenName>
  <foaf:gender>female</foaf:gender>
  <spdemo:zipcode>54360</spdemo:zipcode>
  <spdemo:birthday>19510618</spdemo:birthday>
</rdf:Description>
""")
bios.append("""
<rdf:Description rdf:about="http://smartplatforms.org/records/%s">
  <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
  <foaf:familyName>Dockendorf</foaf:familyName>
  <foaf:givenName>Tad</foaf:givenName>
  <foaf:gender>male</foaf:gender>
  <spdemo:zipcode>82001</spdemo:zipcode>
  <spdemo:birthday>19750705</spdemo:birthday>
</rdf:Description>
""")
bios.append("""
<rdf:Description rdf:about="http://smartplatforms.org/records/%s">
  <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
  <foaf:familyName>Bergermeister</foaf:familyName>
  <foaf:givenName>Nora</foaf:givenName>
  <foaf:gender>female</foaf:gender>
  <spdemo:zipcode>19013</spdemo:zipcode>
  <spdemo:birthday>19641009</spdemo:birthday>
</rdf:Description>
""")
bios.append("""
<rdf:Description rdf:about="http://smartplatforms.org/records/%s">
  <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
  <foaf:familyName>Odenkirk</foaf:familyName>
  <foaf:givenName>Bob</foaf:givenName>
  <foaf:gender>male</foaf:gender>
  <spdemo:zipcode>90001</spdemo:zipcode>
  <spdemo:birthday>19591225</spdemo:birthday>
</rdf:Description>
""")
bios.append("""
<rdf:Description rdf:about="http://smartplatforms.org/records/%s">
  <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
  <foaf:familyName>Richardson</foaf:familyName>
  <foaf:givenName>Douglas</foaf:givenName>
  <foaf:gender>male</foaf:gender>
  <spdemo:zipcode>01040</spdemo:zipcode>
  <spdemo:birthday>19680901</spdemo:birthday>
</rdf:Description>
""")

from smart.views.rdfstore import record_demographics_put_helper


count=1
for b in bios:
  id="sample_patient_%03d"%count
  count += 1
  ss_patient = Record.objects.create(id=id)
  req = Object()
  req.raw_post_data = """<?xml version="1.0"?>
   <rdf:RDF
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:spdemo="http://smartplatforms.org/demographics/"
     xmlns:foaf="http://xmlns.com/foaf/0.1/"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:dcterms="http://purl.org/dc/terms/"
     xmlns:bio="http://purl.org/vocab/bio/0.1/">
   %s
   </rdf:RDF>"""%(b%ss_patient.id)

  record_demographics_put_helper(req,ss_patient)
