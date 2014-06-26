from __future__ import division
import os
from django.shortcuts import render_to_response
from .models import *
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import urllib2
#from bs4 import BeautifulSoup
from django.db import transaction, IntegrityError
from django.utils.text import slugify


@login_required
def plantAdminIndex(request):
    page = 'plantAdminIndex'
    return render_to_response('plantAdminIndex.html', locals(), context_instance=RequestContext(request))


def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)


@login_required
def generateStaticFiles(request):
    header = """
    <!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8" />
<meta name="description" content="Plant species of Tumamoc Hill" />
<meta name="viewport" content="initial-scale=1, maximum-scale=1" />
   <meta name="Author" content="Mike Rosenzweig">
   <title>Flowering plant species of Tumamoc Hill</title>
<style type="text/css">
body {font-family: Trebuchet, Helvetica, Arial, sans-serif; font-size: 13px;}
P.intro {color:#050505; font-size: 11pt; line-height: 1.3em; text-align:left;}
p.intro:first-letter {font-size:180%; font-weight:bold; color:darkgreen}
ul.help {line-height: 1.3em;}
H3 {color:black; font-size:13pt;}
H2 {color:maroon;}
</style>

<link type="text/css" rel="stylesheet" href="../js-css-menu.css" media="screen" />
</head>
<!-- header -->
<body bgcolor="oldlace" text="#000000">

<table align=center width=1000>
<tr><td align=center width=1000>
<ul class="js-css-menu shadow responsive">
	<li>&nbsp;<img src="../Tumamoc icon-OldLace35.jpg">&nbsp;</li>
	<li class="Index"><a href="../Index.html">Home&nbsp;</a>
		<div>
			<ul>
				<li><a href="../about.html">About</a></li>    <li><a href="../Contacts.html">Contacts&nbsp;</a></li>
			</ul>
		</div>
	</li>
	<li class="Events"><a href="../events.html">Events</a>
		<div>
			<ul>
				<li><a href="../calendar.html">Calendar&nbsp;</a></li>    <li><a href="../yours.html">Your event</a></li>
				<li><a href="../newstuff.html">What's new&nbsp;</a></li>
			</ul>
		</div>
	</li>
	<li class="History"><a href="../HISTORY.html">History</a>
		<div>
			<ul>
				<li><a href="../timeline.html"><b>TIME &amp; SPACE</b>&nbsp;</a></li>
				<li><a href="../timeline.html#ancient">Hohokam &amp; before&nbsp;</a></li>
				<li><a href="../timeline.html#EarlyTucson">Early Tucson&nbsp;</a></li>
				<li><a href="../timeline.html#DesertLab">The Desert Lab&nbsp;</a></li>
				<li><a href="../timeline.html#USDA">Forest Service years&nbsp;</a></li>
				<li><a href="../timeline.html#UApurchase">UA buys Tumamoc&nbsp;</a></li>
				<li><a href="../timeline.html#K-12">The school trustland&nbsp;</a></li>
			</ul>
			<ul>
				<li><a href="../people.html"><b>PEOPLE</b>&nbsp;</a></li>
				<li><a href="../Volney.html">Volney Spalding&nbsp;</a></li>
				<li><a href="../Shreve.html">Forrest Shreve</a></li>
				<li><a href="../Lloyd.html">Francis Lloyd</a></li>
				<li><a href="../Sykes.html">Godfrey Sykes&nbsp;</a></li>
				<li><a href="../Burt Bovee.html">Burt Bovee</a></li>
			</ul>
			<ul>
				<li><a href="../stories.html"><b>STORIES</b>&nbsp;</a></li>
				<li><a href="../name.html">What's a <i><b>tumamoc</b></i>?&nbsp;</a></li>
				<li><a href="../tents.html">Tumamocville&nbsp;</a></li>
				<li><a href="../salton.html">The Yacht Club&nbsp;</a></li>
				<li><a href="../ESA.html">Founding the <i>ESA</i>&nbsp;</a></li>
				<li><a href="../cohesive.html">Are ecosystems cohesive?</a></li>
				<li><a href="../saguaroNP.html">Saguaro National Park</a></li>
				<li><a href="../supersykes.html">SuperSykes&nbsp;</a></li>
			</ul>
			<ul>
				<li><a href="../album.html"><b>ALBUM</b>&nbsp;</a></li>
				<li><a href="../photos.html">Photos</a></li>
				<li><a href="../videos.html">Videos</a></li>
				<li><a href="../documents.html">Documents</a></li>
			</ul>
		</div>
	</li>
	<li><a href="../research.html">Research</a>
		<div>
			<ul>
				<li><a href="../research.html#Ecology"><b>ECOLOGY</b>&nbsp;</a></li>
				<li><a href="../plots.html">Spalding plots&nbsp;</a></li>
				<li><a href="../saguaro.html">Saguaro</a></li>
				<li><a href="../data.html">Data sets</a></li>
				<li><a href="../archive.html">Publication archive&nbsp;</a></li>
			</ul>
			<ul>
				<li><a href="../research.html#Conservation"><b>CONSERVATION&nbsp;</b></a></li>
				<li><a href="../restoration.html">Restoration ecology&nbsp;</a></li>
				<li><a href="../reconciliation.html">Reconciliation ecology&nbsp;</a></li>
				<li><a href="../pests.html">Invasive species&nbsp;</a></li>
				<li><a href="../climate.html">Climate change&nbsp;</a></li>
				<li><a href="../urbs.html">Urban ecology&nbsp;</a></li>
			</ul>
			<ul>
				<li><a href="../research.html#Archaeology"><b>ARCHAEOLOGY&nbsp;</b></a></li>
				<li><a href="../plantation.html">Agave plantation</a></li>
				<li><a href="../mesa.html">Village</a></li>
				<li><a href="../trinchera.html">Trincheras</a></li>
			</ul>
		</div>
	</li>
	<li><a href="../community.html">Community</a>
		<div>
			<ul>
				<li><b>GET INVOLVED !&nbsp;</b></li>
				<li><a href="../volunteer.html">Volunteer&nbsp;</a></li>
				<li><a href="../advocate.html">Advocate&nbsp;</a></li>
				<li><a href="../donate.html">Donate&nbsp;</a></li>
				<li><a href="../friends.html"><i>Friends of the Hill</i>&nbsp;</a></li>
			</ul>
			<ul>
				<li><a href="../Hiking.html">Walkers&nbsp;</a></li>
<li><a href="../docents.html">Docents&nbsp;</a></li>    <li><a href="../CitizenScience.html">Citizen Science</a></li>
				<li><a href="../TBC.html"><i>Tucson Bird Count</i></a></li>
				<li><a href="../transform.html">New Ecosystems</a></li>
			</ul>
		</div>
	</li>

	<li><a href="../Education.html"><font color=tomato size="+1">EDUCATION</font></a>
		<div>
			<ul>
				<li><a href="../courses.html">University classes&nbsp;</a></li>
				<li><a href="../tusd.html">Schools&nbsp;</a></li>
<li><a href="../docents.html">Docents&nbsp;</a></li>    <li><a href="../CitizenScience.html">Citizen Science</a></li>
				<li><a href="../lectures.html">Lectures in the Library&nbsp;</a></li>
			</ul>
			<ul>
				<li><a href="../diversity.html"><b>LIFE FORMS&nbsp;</a></b></li>
				<li><a href="../Plants.html">Plants&nbsp;</a></li>
				<li><a href="../animals.html">Animals&nbsp;</a></li>
						<!-- ul>
							<li><a href="../#">Birds</a></li>
							<li><a href="../#">Mammals</a></li>
							<li><a href="../#">Spiders & insects</a></li>
						</ul -->
			</ul>
		</div>
	</li>
	<li><a href="../Arts.html">Arts</a>
		<div>
			<ul>
				<li><a href="../Mirochaframes.html">Tumamoc Sketchbook&nbsp;</a></li>
				<li><a href="../gallery.html">Hill Gallery&nbsp;</a></li>
				<li><a href="../writing.html">Poetry/prose&nbsp;</a></li>
				<li><a href="../music.html">Music&nbsp;</a></li>
			</ul>
		</div>
	</li>
	<li><a href="../onward.html">Onward</a>
	<div>
			<ul>
				<li><a href="../developingPrograms.html">Developing Programs</a></li>
				<li><a href="../appeal.html">Dreams</a></li>
			</ul>
		</div>
	</li>
</ul>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</table>

<table align="center" valign="top" border="0" cellspacing="2" cellpadding="3" width="700">

<tr><td align="center" valign=top width="700">

<h1>Flowering perennial plant species of Tumamoc Hill</h1>

<p class="intro">Tumamoc has more than 300 species of perennial flowering plants. Thanks to the artistry, hard work and generosity of T. Beth Kinsey, you can already see 130 of them in this part of the website.</p>
<p class="intro">The species list below has all our species but many do not yet have their own webpage. We are working to include them, too. (Check the <a href="http://tumamoc.org/newstuff.html" STYLE="text-decoration: none" target="_blank">What's new?</a> page for notice of additions.)</p>
<p class="intro">Meanwhile, visit Beth's own site <a href="http://fireflyforest.com/flowers" STYLE="text-decoration: none" target="_blank">Fireflyforest</a> where you will find other plants of southern Arizona, as well as many from Hawaii. And please do let Beth know how much you appreciate her work!</p>

</td></tr>
</table>
<!-- end of header -->"""

    footer = """<!-- footer -->
<table align=center width=720>
<tr><td><hr color=darkgreen></td></tr>
<tr><td><p><font size="+1"><center>Tumamoc is retooling to meet the challenges and opportunities of its second century.
<br>Your support can make these plans a reality.</center></font></p>
</td></tr>
</table>

<table align=center width=600>

<tr><td align="center" valign=top width=305><a href="../appeal.html"><img src="../ActNow300.jpg" width="300" height="278" border=1 alt="" /><a/></td>

<td align="center" width=300><font size="3" face="Times,Georgia" color="#000000"><b>
Help Tumamoc extend its timeline throughout the 21<sup>st</sup> century<br>and beyond.
			<blockquote><ul class="help">
<li><a href="../volunteer.html">Volunteer&nbsp;</a></li>
<li><a href="../appeal.html">Support&nbsp;</a></li>
<li><a href="../advocate.html">Advocate&nbsp;</a></li>
<li><a href="../friends.html">Join <i>Friends of the Hill</i>&nbsp;</a></li>
			</ul></blockquote>
</b></font></td></tr>
</table>

<table width=600 border=0 cellpadding=0 align="center" valign=top cellspacing=0>
<tr bgcolor=#456709; valign="center" height="35" width=692 border=0>
<td height="35"><img src="../Tumamoc icon-OldLace35.jpg"></td>
<td height="35"><font face=Trebuchet, "Times New Roman","sans-serif" color=peachpuff>
<b>&nbsp;Tumamoc is managed by the University of Arizona College of Science and Pima County, Arizona.</b>
</td></tr>
</table>

<!-- end of footer -->"""
    body = "<ul>"
    daveMessage = ""
    detailBody = ""
    detailOutput = ""
    plants = Plant.objects.all()
    for plant in plants:
        try:
            #detailBody = plant.firefly_set.get().firefly_html  #this works, but less explicit
            plantId = plant.id
            ff = Firefly.objects.get(firefly_plant=plantId)
            detailBody = ff.firefly_html
            detailOutput = removeNonAscii(header + detailBody + footer)
        except:
            detailBody = "<h2>" + plant.common_name + "</h2>"
            detailBody = "<h3><i>" + plant.genus + " " + plant.species + "</i> (" + plant.family + ")</h3>"
            detailBody += "<p>Sorry we do not have a plant detail page prepared for this plant yet.  Coming Soon.</p>"
            detailOutput = removeNonAscii(header + detailBody + footer)
            daveMessage += "<p>oops no data or error on plant = " + plant.common_name + "</p>"
        fDetail = "plantlist/" + plant.slug + ".html"
        fnameDetail = os.path.join(settings.MEDIA_ROOT, fDetail)
        print fnameDetail
        fd = open(fnameDetail, 'w')
        fd.write(detailOutput)
        fd.close()
        #thisline = '<li><a href="/plants/details/' + plant.slug + '/">'
        thisline = '<li><a href="' + plant.slug + '.html">'
        thisline += plant.common_name + "</a> <i>" + plant.genus + " " + plant.species
        thisline += "</i> (" + plant.family + ")</li>\n"
        body += thisline
    body += "</ul>"
    output = header + body + footer
    fname = os.path.join(settings.MEDIA_ROOT, "plantlist/index.html")
    f = open(fname, 'w')
    f.write(output)
    f.close()

    daveMessage = "<h3>Done generating static plant list files.</h3>" + daveMessage
    return render_to_response('plantAdminIndex.html', locals(), context_instance=RequestContext(request))




def fetchFromFirefly(request):
    #/plantadmin/fetch-from-firefly/
    daveMessage = ""
    ffplants = Plant.objects.exclude(firefly_url__isnull=True).exclude(firefly_url__exact='')
    for plant in ffplants:
        try:
            url = plant.firefly_url
            page = urllib2.urlopen(url)
            html = page.read()
            start = '<div class="post"'
            startpos = html.find(start)
            html = html[startpos:]
            end = '<!-- END postbg -->'
            endpos = html.find(end)
            html = html[:endpos]
            html = u(html)
            cleanhtml = str(html)
            ff = Firefly()
            ff.firefly_plant = plant
            ff.firefly_html = cleanhtml
            ff.save()
        except:
            daveMessage += "<p>Error on url " + url + "</p"
    return render_to_response('plantAdminIndex.html', locals(), context_instance=RequestContext(request))


def parseOutFirefly(request):
    daveMessage = ""
    ffplants = Firefly.objects.all()
    for plant in ffplants:
        try:
            html = plant.firefly_html
            plant.firefly_growth_habit = parseOut(html, '<span>Growth Habit:</span>', '</p>')
            plant.firefly_habitat = parseOut(html, '<span>Habitat:</span>', '</p>')
            plant.firefly_duration = parseOut(html, '<span>Duration:</span>', '</p>')
            plant.firefly_native_status = parseOut(html, 'Native Status:</span>', '</p>')
            plant.firefly_flower_color = parseOut(html, '<span>Flower Color:</span>', '</p>')
            plant.firefly_flower_season = parseOut(html, '<span>Flowering Season:</span>', '</p>')
            plant.firefly_height = parseOut(html, '<span>Height:</span>', '</p>')
            print plant.firefly_height
            index = html.find('Special Characteristics</p>')
            if index > 0:
                plant.firefly_special = parseOut(html, 'Special Characteristics</p>', '<p class="special">Classification')
            plant.firefly_description = parseOut(html, '<span>Description:</span>', '</p>')
            plant.firefly_class = parseOut(html, '<span>Subclass:</span>', '<br />')
            plant.firefly_subclass = parseOut(html, '<span>Duration:</span>', '<br />')
            plant.firefly_order = parseOut(html, '<span>Order:</span>', '<br />')
            print plant.firefly_order
            try:
                plant.save()
            except IntegrityError:
                transaction.rollback()
        except:
            daveMessage += "<p>Error on plant " + plant.firefly_plant.common_name + "</p>"
            print "<p>Error on plant " + plant.firefly_plant.common_name + "</p>"
    return render_to_response('plantAdminIndex.html', locals(), context_instance=RequestContext(request))



def parseOut(source, start, end):
    startpos = source.find(start)
    startpos = startpos + len(start) + 1
    output = source[startpos:]
    endpos = output.find(end)
    output = output[:endpos]
    return output


def redoSlugs(request):
    plants = Plant.objects.all()
    for plant in plants:
        s = plant.species
        g = plant.genus
        slug = slugify(g + '-' + s)
        plant.slug = slug
        plant.save()
        daveMessage = "<h2>All done re-doing slugs.</h2>"
    return render_to_response('plantAdminIndex.html', locals(), context_instance=RequestContext(request))


def processFireflyData(request):
    fname = os.path.join(settings.MEDIA_ROOT, "fireflyData.tab")
    print fname
    output = ""
    with open(fname, 'rU') as f:
        lines = f.readlines()
    print "lines = "
    for line in lines:
        fields = line.split('\t')
        try:
            sciName = fields[1]
            ffUrl = fields[0]
            names = sciName.split(' ')
            try:
                thisPlant = Plant.objects.get(genus=names[0],species=names[1])
                print "thisPlant species is " + thisPlant.species
                print "thisPlant family is " + thisPlant.family
                print "ffUrl = " + ffUrl
                print "thisPlant url start " + str(thisPlant.firefly_url)
                thisPlant.firefly_url = ffUrl
                print "thisPlant url is NOW " + thisPlant.firefly_url
                thisPlant.save()
            except:
                output += "<p>could not find sciName: {0} {1}</p>".format(names[0],names[1])
        except:
            pass
    return render_to_response('report.html', locals(), context_instance=RequestContext(request))
