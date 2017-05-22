# -*- coding: utf-8 -*-

"""
OMWebbook is a An OpenModelica interactive notebook online. The Webbook is generated 
with the help of Flask framework.This file is used for the conversion of DrModelica exercise files 
to HTML Files with some control over the numbering of sections and subsections
"""

__license__ = """
 This file is part of OpenModelica.

 Copyright (c) 1998-CurrentYear, Open Source Modelica Consortium (OSMC),
 c/o Linköpings universitet, Department of Computer and Information Science,
 SE-58183 Linköping, Sweden.

 All rights reserved.

 THIS PROGRAM IS PROVIDED UNDER THE TERMS OF THE BSD NEW LICENSE OR THE
 GPL VERSION 3 LICENSE OR THE OSMC PUBLIC LICENSE (OSMC-PL) VERSION 1.2.
 ANY USE, REPRODUCTION OR DISTRIBUTION OF THIS PROGRAM CONSTITUTES
 RECIPIENT'S ACCEPTANCE OF THE OSMC PUBLIC LICENSE OR THE GPL VERSION 3,
 ACCORDING TO RECIPIENTS CHOICE.

 The OpenModelica software and the OSMC (Open Source Modelica Consortium)
 Public License (OSMC-PL) are obtained from OSMC, either from the above
 address, from the URLs: http://www.openmodelica.org or
 http://www.ida.liu.se/projects/OpenModelica, and in the OpenModelica
 distribution. GNU version 3 is obtained from:
 http://www.gnu.org/copyleft/gpl.html. The New BSD License is obtained from:
 http://www.opensource.org/licenses/BSD-3-Clause.

 This program is distributed WITHOUT ANY WARRANTY; without even the implied
 warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE, EXCEPT AS
 EXPRESSLY SET FORTH IN THE BY RECIPIENT SELECTED SUBSIDIARY LICENSE
 CONDITIONS OF OSMC-PL.
 
 Author : Arunkumar Palanisamy, arunkumar.palanisamy@liu.se
"""


import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding("utf-8")
import re
import string
import numpy
from numpy import array
import struct
import base64

def parsetags(all_tags,f):
    global sectioncheck,subsectioncheck,currentlevel,subsectioncount,g,g1,r,sectioncount,check
    if (all_tags.tag=='TextCell'):
              html=all_tags.find('Text').text
              soup = BeautifulSoup(html)
              for a in soup.findAll('a'):
                 staticlink="".join(['static','/',a['href']]).replace('.onb','.html')
                 a['href']=a['href'].replace(a['href'], staticlink)                 
                 #print staticlink              
              #findp=soup.find_all('p')
              
              findp=[]
              for p in soup.findAll('p'):
                 checkempty=p['style'].replace(' ','').split(";")
                 val="-qt-paragraph-type:empty" in checkempty
                 if (val==False):
                    if (p.find('img')==None):
                        findp.append(p)
               
              for i in xrange(len(findp)):
                   #x=findp[i].text
                   x=findp[i]
                   x=re.sub(r'[^\x00-\x7F]+',' ', str(x))
                   if(x!=''):
                     val=findp[i].text
                     '''
                     if(val=='Answer'):
                        global r
                        target='#answer'+str(r)
                        btn=" ".join(['<button type= button class= btn btn-info data-toggle= collapse data-target=',str(target),'>','Answer</button>'])
                        print btn
                     print val'''
                     if(all_tags.attrib['style']=='Text'):
                        #partext='\n'.join(['<p align="justify" contenteditable=False>',str(x),'</p>'])
                        partext='\n'.join([str(x)])
                        f.write(partext)
                        f.write('<br>')
                        f.write('\n')
                     
                     elif(all_tags.attrib['style']=='Title'):
                        print 'title'
                        t=findp[i].text
                        t=re.sub(r'[^\x00-\x7F]+',' ', str(t))
                        htmltext='\n'.join(['<h1>',t,'</h1>'])
                        #htmltext='\n'.join([str(x)])
                        f.write(htmltext)
                        f.write('\n')
                     
                     elif(all_tags.attrib['style']=='Section'):
                        print 'section'
                        t=findp[i].text
                        t=re.sub(r'[^\x00-\x7F]+',' ', str(t))
                        if(t=='Answer'):
                            target='#answer'+str(r)
                            t=" ".join(['<button type= button class= "btn btn-info" data-toggle= "collapse" data-target=',str(target),'>','Answer</button>'])
                        sectioncheck=True
                        htmltext='\n'.join(['<h2>',str(sectioncount),t,'</h2>'])
                        sectioncount+=1
                        #htmltext='\n'.join([str(x)])
                        f.write(htmltext)
                        f.write('\n')
                     elif(all_tags.attrib['style']=='Subsection'):
                       
                        if(sectioncheck==True):
                            g=1
                        g+=1
                        sectioncheck=False
                        #print 'subsection',sectioncheck,(sectioncount-1),'.',(g-1)
                        subsec=findp[i].text
                        subsec=re.sub(r'[^\x00-\x7F]+',' ', str(subsec))
                        if(subsec=='Answer'):
                            target='#answer'+str(r)
                            subsec=" ".join(['<button type= button class="btn btn-info" data-toggle="collapse" data-target=',str(target),'>','Answer</button>'])

                        #scount=(sectioncount-1)+subsectioncount
                        scount=str((sectioncount-1))+'.'+str((g-1))
                        subsectioncheck=True
                        currentlevel=scount
                        #print str((sectioncount-1)),'.',g
                        #print 'subsection',scount
                        htmltext='\n'.join(['<h3>',str(scount),subsec,'</h3>'])
                        subsectioncount+=0.01
                        #htmltext='\n'.join([str(x)])
                        f.write(htmltext)
                        f.write('\n')
                     elif(all_tags.attrib['style']=='Subsubsection'):
                        if(subsectioncheck==True):
                            g1=1
                        g1+=1
                        subsectioncheck=False
                        #print 'subsection',sectioncheck,(sectioncount-1),'.',(g-1)
                        subsec=findp[i].text
                        subsec=re.sub(r'[^\x00-\x7F]+',' ', str(subsec))
                        if(subsec=='Answer'):
                            target='#answer'+str(r)
                            subsec=" ".join(['<button type= button class="btn btn-info" data-toggle="collapse" data-target=',str(target),'>','Answer</button>'])
                        #scount=(sectioncount-1)+subsectioncount
                        scount=str(currentlevel)+'.'+str((g1-1))
                        print 'subsubsection',scount
                        #print str((sectioncount-1)),'.',g
                        #print 'subsection',scount
                        htmltext='\n'.join(['<h4>',str(scount),subsec,'</h4>'])
                        subsectioncount+=0.01
                        #htmltext='\n'.join([str(x)])
                        f.write(htmltext)
                        f.write('\n')
                     else:
                        htmltext='\n'.join(['<h1>',str(x),'</h1>'])
                        #htmltext='\n'.join([str(x)])
                        f.write(htmltext)
                        f.write('\n')

    if (all_tags.tag=='GraphCell' or all_tags.tag=='InputCell'):
              ## catch the input text
              inputtext=all_tags.find('Input').text
              print 'inputcells',inputtext
              if(inputtext!=None):
                  linecount=string.split(inputtext, '\n')            
                  textid='check'+str(check)+'textarea'
                  divid='check'+str(check)+'div'
                  if ('plot(' in inputtext):
                     text='\n'.join(['<textarea id='+ str(textid)+'>',inputtext,'</textarea> <br> <div id='+divid+'> </div> <br>'])
                  else:
                     text='\n'.join(['<textarea id='+ str(textid)+'>',inputtext,'</textarea>  <div id='+divid+'> </div> <br>'])
                  check=check+1
                  f.write(text)
                  f.write('\n')
                  ## catch the OMCPLOT datas
                  curve=all_tags.find('OMCPlot')
                  
                  if curve!=None:
                     #count=count+1;
                     print count
                     try:
                       #scriptdata=makeplot(curve,count)
                       scriptdata=makeplot(curve,divid)
                       f.write(scriptdata)
                       f.write('\n')
                     except:
                       f.write("No data found")
                       f.write('\n')
              else:
                  textid='check'+str(check)+'textarea'
                  divid='check'+str(check)+'div'
                  inputtext=''
                  text='\n'.join(['<textarea id='+ str(textid)+'>',inputtext,'</textarea>  <div id='+divid+'> </div> <br>'])
                  check=check+1
                  f.write(text)
                  f.write('\n')

                  print "Empty Graph cells"
        
def makeplot(curve,graphdivid):
     datas=curve.findall('Curve')
     plotdata=[]
     labeldata=['Time']
     for i in xrange(len(datas)):
       datas1=datas[i].attrib
       xcurve=datas1['XData']
       ycurve=datas1['YData']
       label=datas1['Title']
       xdata_bytes = base64.b64decode(xcurve)
       ydata_bytes = base64.b64decode(ycurve)
       xdata= [struct.unpack_from('>d', xdata_bytes, offset) for offset in range(0, len(xdata_bytes), 8)]
       ydata= [struct.unpack_from('>d', ydata_bytes, offset) for offset in range(0, len(ydata_bytes), 8)]
       if (i==0):
          plotdata.append(xdata)
       plotdata.append(ydata)
       labeldata.append(label)
       
     if (len(plotdata) !=0):
        n=array(plotdata)
        #print 'plotdata', plotdata
        numpy.set_printoptions(threshold='nan')
        #print repr(numpy.hstack(n))
        try:        
           dygraph_array= repr(numpy.hstack(n)).replace('array',' ').replace('(' ,' ').replace(')' ,' ')
           return writedygraphscript(dygraph_array,labeldata,graphdivid)
        except ValueError:
           print 'Value Error'
           return writedygraphscript('ValueError',labeldata,graphdivid)

        
def writedygraphscript(dygraphdata,labeldata,graphdivid):
   
     #divheader= '''<script type="text/javascript" src="../dygraph-combined.js"></script>'''
     #<div id="graphdiv"></div>                
     #<script type="text/javascript">
     #g = new Dygraph(document.getElementById("graphdiv"),'''
     #divid='<div id=graphdiv'+str(count)+'>'+'</div>'
     #divid='<div id='+ graphdivid + '> </div>'
     #divgraph='g = new Dygraph(document.getElementById("graphdiv'+str(count)+'"),' 
     divgraph='g = new Dygraph(document.getElementById('+'"'+str(graphdivid)+'"'+'),'
     scriptheader='\n'.join(['<script type="text/javascript">',divgraph])
     options='\n'.join(['{', 'legend:"always",','labels:',str(labeldata),'}'])
     s = '\n'.join([scriptheader,str(dygraphdata),',',options,')','</script>'])
     return s              

def start(filename,root):
        global sectioncheck,subsectioncheck,currentlevel,subsectioncount,g,g1,r,sectioncount,check
        logdir='C:/OMWebbook/static/Circuits'
        name= os.path.basename(filename)
        logfile=os.path.join(logdir,name.replace('.onb','.html')).replace('\\','/')   
        print logfile
        f=open(logfile,'w')
        headers='''  
<!doctype html>
<head>
  <title>OMWEBbook</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="../jquery.min1.10.2.js"></script>
  <script src='../dygraph-combined.js'></script>
  <link rel="stylesheet" href="../bootstrap.min.css">
  <script src="../bootstrap.min.js"></script>
  <link rel="stylesheet" href="../codemirror.css">
 <script src="../codemirror.js"></script>
 <script src="../modelica.js"></script>
 <link rel="stylesheet" href="../custom.css">
  <script src="../autorefresh.js"></script>
  <script src="../evalnotebook.js"></script>
</head>


<body>
<div class="navbar navbar-default navbar-fixed-top">
  <div class="container-fluid">
    <div class="navbar-header">
      <a class="navbar-brand" href="#">OMWebBook</a>
    </div>
     <button id="evaluate" type="button" class="btn btn-success navbar-btn">Evaluate Cell</button>
    <button id="evaluateall" type="button" class="btn btn-success navbar-btn">Eval All</button>
    <img id="progressbar" src="../ajax-loader.gif" class="img-rounded" alt="Cinque Terre">
  </div>
</div>
<div class="container">
<br> <br> <br>

'''
        f.write(headers)     
        for node in root.iter('GroupCell'):
            #print node.tag
            if node.tag=='GroupCell' and node.attrib['closed']=='false':     
                for all_tags in node.findall('./'):
                     parsetags(all_tags,f)
            
            if node.tag=='GroupCell' and node.attrib['closed']=='true':
                #print '<div>'
                c=0
                for all_tags in node.findall('./'):
                     #print all_tags.tag,all_tags.attrib
                     if(c==1):
                        global r
                        dividanswer='<div id=answer'+ str(r) +' '+'class=collapse>'
                        f.write(dividanswer)                        
                        print dividanswer
                     parsetags(all_tags,f)
                     c+=1
                r+=1
                f.write('</div>')
                print '</div>'
                print '******closed_end'
        f.write('</div></body></html>')
        f.close()         
        print 'Completed'
        print 'after completion',r
        r=0
        count=0
        check=0
        sectioncount=1      
        subsectioncount=0.01
        sectioncheck=False
        subsectioncheck=False
        currentlevel=''
        g=1
        g1=1  


        
r=0
count=0
check=0
sectioncount=1      
subsectioncount=0.01
sectioncheck=False
subsectioncheck=False
currentlevel=''
g=1
g1=1  

            
if __name__ == "__main__":
    
    dir1='C:/OPENMODELICAGIT/OpenModelica/OMNotebook/DrModelica/Circuits'
    filelist=os.listdir(dir1)
    #print filelist
    for i in xrange(len(filelist)):
        name=filelist[i]
        filename=os.path.join(dir1,name).replace('\\','/')
        tree = ET.parse(filename)
        root = tree.getroot()                  
        start(filename,root)
    '''
    filename='C:/OPENMODELICAGIT/OpenModelica/OMNotebook/DrModelica/QuickTour/Exercise1arrays.onb'
    tree = ET.parse(filename)
    #tree = ET.parse('C:/OPENMODELICAGIT/OpenModelica/build/share/omnotebook/drmodelica/QuickTour/HelloWorld.onb')
    #Exercise1classes
    root = tree.getroot()                  
    start(filename,root) 
    
    filename='C:/OPENMODELICAGIT/OpenModelica/OMNotebook/DrModelica/QuickTour/Exercise1classes.onb'
    tree = ET.parse(filename)
    root = tree.getroot()  
    start(filename,root) '''    