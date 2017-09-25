# -*- coding: utf-8 -*-

"""
OMWebbook is a An OpenModelica interactive notebook online. The Webbook is generated 
with the help of Flask framework.This file is used for the conversion of DrModelica files 
to HTML Files.
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
from PySide.QtCore import QBuffer, QIODevice, QDataStream, QByteArray
from PySide import QtGui, QtCore
import uuid

def runparser(filelistdirs,logdir):
  print 'Start running the Translator'
  #os.chdir(logdir)
  filelistdirs=filter(None,filelistdirs)
  print 'D1',filelistdirs
  for dir in xrange(len(filelistdirs)):
    curdir=filelistdirs[dir]
    print 'D2',curdir
    newdir=os.path.join(logdir,os.path.basename(curdir)).replace('\\','/')
    if not os.path.exists(newdir): 
          os.mkdir(newdir)
    filelist = os.listdir(curdir) 
    print filelist 
    os.chdir(curdir)
    for z in xrange(len(filelist)):
        ### Start the xml parser 
        tree = ET.parse(filelist[z])
        root = tree.getroot()
        
        '''create a html result file '''
        filename= os.path.basename(filelist[z])
        logfile=os.path.join(newdir,filename.replace('.onb','.html')).replace('\\','/')   
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
        count=0
        check=0
        sectioncount=1      
        subsectioncount=0.01
        sectioncheck=False
        subsectioncheck=False
        currentlevel=''
        g=1
        g1=1        
        for node in tree.iter():
           if (node.tag=='TextCell'):
              imagelist=node.findall('Image')
              html=node.find('Text').text
              soup = BeautifulSoup(html)
              for a in soup.findAll('a'):
                 staticlink="".join(['static','/',a['href']]).replace('.onb','.html')
                 a['href']=a['href'].replace(a['href'], staticlink)                 
                 #print staticlink
                  
              findp=[]
              for p in soup.findAll('p'):
                 checkempty=p['style'].replace(' ','').split(";")
                 val="-qt-paragraph-type:empty" in checkempty
                 if (val==False):
                    # if (p.find('img')==None):
                        # findp.append(p)
                    # else:
                        findp.append(p)
              for i in xrange(len(findp)):
                   #x=findp[i].text
                   x=findp[i]
                   if(x.find('img')is None):
                       if(x!=''):
                         if(node.attrib['style']=='Text'):
                            #partext='\n'.join(['<p align="justify" contenteditable=False>',str(x),'</p>'])
                            #x["align"]='justify'
                            x=re.sub(r'[^\x00-\x7F]+',' ', str(x))
                            partext='\n'.join([str(x)])
                            f.write(partext)
                            f.write('<br>')
                            f.write('\n')
                         
                         elif(node.attrib['style']=='Title'):
                            print 'title'
                            t=findp[i].text
                            t=re.sub(r'[^\x00-\x7F]+',' ', str(t))
                            htmltext='\n'.join(['<h1>',t,'</h1>'])
                            #htmltext='\n'.join([str(x)])
                            f.write(htmltext)
                            f.write('\n')
                         
                         elif(node.attrib['style']=='Section'):
                            print 'section'
                            t=findp[i].text
                            t=re.sub(r'[^\x00-\x7F]+',' ', str(t))
                            sectioncheck=True
                            htmltext='\n'.join(['<h2>',str(sectioncount),t,'</h2>'])
                            sectioncount+=1
                            #htmltext='\n'.join([str(x)])
                            f.write(htmltext)
                            f.write('\n')
                         elif(node.attrib['style']=='Subsection'):
                            if(sectioncheck==True):
                                g=1
                            g+=1
                            sectioncheck=False
                            #print 'subsection',sectioncheck,(sectioncount-1),'.',(g-1)
                            subsec=findp[i].text
                            subsec=re.sub(r'[^\x00-\x7F]+',' ', str(subsec))
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
                         elif(node.attrib['style']=='Subsubsection'):
                            if(subsectioncheck==True):
                                g1=1
                            g1+=1
                            subsectioncheck=False
                            #print 'subsection',sectioncheck,(sectioncount-1),'.',(g-1)
                            subsec=findp[i].text
                            subsec=re.sub(r'[^\x00-\x7F]+',' ', str(subsec))
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
                   else:
                       try:
                           imagedir=os.path.join(newdir,"Images").replace('\\','/')
                           if not os.path.exists(imagedir): 
                               os.mkdir(imagedir)
                           os.chdir(imagedir)
                           y=imagelist[0]
                           image=y.text
                           unique_filename = str(uuid.uuid4())
                           img = QtGui.QImage()
                           #image=node.find('Image').text
                           byteArray = QByteArray.fromBase64(image)
                           buffer = QBuffer(byteArray)
                           buffer.open(QIODevice.ReadOnly)
                           data   = QDataStream(buffer)
                           data >> img
                           buffer.close()
                           filename=".".join([unique_filename,"png"])
                           imgpath="/".join(['static',os.path.basename(newdir),'Images/'])
                           imgsrc=imgpath+filename
                           img.save(filename)
                           imgtag="".join(["<div align=\"center\">","<img src=",imgsrc,">","</div>"])
                           #print filename
                           f.write(imgtag)
                           del imagelist[0]
                       except:
                           pass                   
           if (node.tag=='GraphCell' or node.tag=='InputCell'):
              ## catch the input text
            inputtext=node.find('Input').text
            '''
            if ('simulate' in inputtext):
                  text='\n'.join(['<p> <b>',inputtext,'</b> </p>']) 
                  f.write(text)
                  f.write('\n')''' 
            #print 'arun', inputtext
            if(inputtext!=None):
                  linecount=string.split(inputtext, '\n')            
                  '''
                  if ('plot(' in inputtext):
                  text='\n'.join(['<p> <b>',inputtext,'</b> </p> <br>'])  
                  f.write(text)
                  f.write('\n') 
                  ## code to automatically generate plot variable and button in html  
                  plotvar=inputtext.replace('plot','').replace('(','').replace(')','').replace('{','').replace('}','')
                  listplotvar=plotvar.split(',')  
                  plotid='simulatebutton'+str(count)+'plot'
                  buttonid='simulatebutton'+str(count)
                  graphdivid='simulatebutton'+str(count)+'graphdiv'
                  plotheader="\n".join(['<div>','<select id='+ plotid +' size=5 multiple>', '<option ><b>Select Plot Variables</b> </option>'])       
                  f.write(str(plotheader))
                  f.write('\n')
                  for i in xrange(len(listplotvar)):
                     varname='<option selected>'+ str(listplotvar[i]) + '</option>'
                     f.write(varname)
                     f.write('\n')             
                  closeoption="\n".join(['</select> <br>','<button id='+buttonid+'>Simulate</button> <br> <br>' ,'</div>'])
                  f.write(closeoption)
                  count=count+1;
                  else:'''
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
                  curve=node.find('OMCPlot')
                  
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
        f.write('</div></body></html>')
        f.close()         
    print 'Completed'



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
        
       
class CompareListControl(QtGui.QDialog):
        ''' Class for taking onb files '''
        def __init__(self):
            QtGui.QDialog.__init__(self)
            self.setModal(False)
            self.setWindowTitle("Compare Result Files")
            mainGrid = QtGui.QGridLayout(self)
            self.setdir=''
            changeDir = QtGui.QPushButton("setworkdir", self)
            mainGrid.addWidget(changeDir, 0, 1)
            
            self.listdir = QtGui.QLabel("List of Notebook files:", self)
            mainGrid.addWidget(self.listdir , 1, 0, QtCore.Qt.AlignRight)
            self.filelist = QtGui.QListWidget(self)
            self.filelist.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            #self.directory.setFixedHeight(80)
            mainGrid.addWidget(self.filelist, 1, 1, 2, 1)
            
            browseDir1 = QtGui.QPushButton("Select", self)
            mainGrid.addWidget(browseDir1, 1, 2)
            
            self.removeButton = QtGui.QPushButton("Remove", self)
            mainGrid.addWidget(self.removeButton, 2, 2)
            self.removeButton.clicked.connect(self.remove)
            
            result = QtGui.QLabel("Report Directory:", self)
            mainGrid.addWidget(result, 3, 0, QtCore.Qt.AlignRight)
            self.resultEdit = QtGui.QLineEdit("", self)
            mainGrid.addWidget(self.resultEdit, 3, 1)
            browseResult = QtGui.QPushButton("Select", self)
            mainGrid.addWidget(browseResult, 3, 2)
            
            self.runButton = QtGui.QPushButton("Run", self)
            mainGrid.addWidget(self.runButton, 4, 1)
            self.runButton.clicked.connect(self.run)
            self.closeButton = QtGui.QPushButton("Close", self)
            mainGrid.addWidget(self.closeButton, 4, 2)
            self.closeButton.clicked.connect(self.close)
            
            def _browseDir1Do():
               #(fileNames, trash) = QtGui.QFileDialog().getOpenFileNames(self, 'Open Notebook File', os.getcwd(), '(*.onb)')
               dirName = QtGui.QFileDialog().getExistingDirectory(self, 'Select Directory of Results',self.setdir)
               self.filelist.addItem(dirName)
               '''
               for fileName in fileNames:
                  fileName = fileName.replace('\\', '/')
                  if fileName != '':
                    self.filelist.addItem(fileName)'''

            def _browseResultDo():
                #(fileName, trash) = QtGui.QFileDialog().getSaveFileName(self, 'Define Analysis Result File', os.getcwd(), '(*.log);;All Files(*.*)')
                dirName = QtGui.QFileDialog().getExistingDirectory(self, 'Select Directory of Results',self.setdir)
                dirName = dirName.replace('\\', '/')
                if dirName != '':
                    self.resultEdit.setText(dirName)
            
            def changedirdo():
                #(fileName, trash) = QtGui.QFileDialog().getSaveFileName(self, 'Define Analysis Result File', os.getcwd(), '(*.log);;All Files(*.*)')
                dirName = QtGui.QFileDialog().getExistingDirectory(self, 'Select workdir')
                self.setdir=dirName
                #os.chdir(dirName)
            
            changeDir.clicked.connect(changedirdo)
            browseDir1.clicked.connect(_browseDir1Do)
            browseResult.clicked.connect(_browseResultDo)
            
            self.show()
            
        def run(self):
        
            # Get data from GUI
            logDir = self.resultEdit.text()
            
            notebookfilelist=[]
            sitems=self.filelist.selectedItems()
            if(len(sitems)!=0):
               for item in self.filelist.selectedItems():        
                  notebookfilelist.append(item.text())
            else:
               for i in xrange(self.filelist.count()):
                 item=self.filelist.item(i).text()
                 notebookfilelist.append(item)

            # Run the analysis
            if (len(notebookfilelist)!=0):
                #gui._compareThreadTesting = runCompareResultsInDirectories(gui.rootDir, dir1, listdirs, tol, logDir)
                runparser(notebookfilelist,logDir)
            else:
                print 'No files Selected'

         
        def remove(self):
           listItems=self.filelist.selectedItems()
           if not listItems: return        
           for item in listItems:
               self.filelist.takeItem(self.filelist.row(item))  
        
                
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ex = CompareListControl()
    sys.exit(app.exec_())
    '''
    dir1=["C:\\Users\\rain1_000\\Desktop\\pythonscript\\test"]
    dir2="C:\\Users\\rain1_000\\Desktop\\pythonscript\\static"
    runparser(dir1,dir2)'''
       