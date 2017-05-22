# -*- coding: utf-8 -*-
"""
OMWebbook is a An OpenModelica interactive notebook online. The Webbook is generated 
with the help of Flask framework.
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

from flask import Flask, jsonify, render_template, request,session
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import numpy
from numpy import array
import shutil
from OMPython import OMCSession
import tempfile
import re
app = Flask(__name__)
app.secret_key = 'c\x9e\xdf\xf4\xfc\x15\x84A\xc3\xda\x8d\xdf\xbd\x10\x07\x88C\x10L\xff\xc6h&\n'

sessionobj={}
mat=[]

@app.route('/')
def index():
    return render_template('Top.html')

@app.route('/DrModelica', methods=['GET','POST'])
def DrModelica():
    #if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        # return redirect(url_for('index'))
    # show the form, it wasn't submitted
    return render_template('index.html')    

@app.route('/evalexpression', methods=['POST'])
def evalexpression():
    #print 'inside eval'
    try:
        text_content=request.form['input']
        div_content =request.form['output']
        sidcheck=request.form['sid'] 
        #print sidcheck 
        getomcobj=sessionobj[sidcheck]
        #sys.stdout.flush()    
        eval(text_content,div_content,getomcobj)    
        data="\n".join(session['msg'])
        del session['msg'][:]     
        return data 
    except:
        return "failed"    
	
@app.route('/createsession', methods=['POST'])
def createsession():
        ## Create a new omc session for the users and allot a seperate working directory for the session ##
        #print 'creating omc session'
        session['msg']=[]
        session['mat']=[]
        sid=request.form['sid']
        session['tmpdir'] = tempfile.mkdtemp()
        #print session['tmpdir'] 
        os.chdir(session['tmpdir'])
        sess=OMCSession()
        sessionobj[sid]=sess
        #print sessionobj
        #sys.stdout.flush()
        return "success"

@app.route('/deletesession', methods=['POST'])
def deletesession():
       ## delete the omc object and process when the user leaves the browser ##
       #print "Deleting"
       os.chdir("..")
       sid1=request.form['sid']
       if (len(sessionobj)!=0):
           omcobj=sessionobj[sid1]
           #print omcobj.sendExpression("getClassNames()")
           omcobj.__del__()
           #print 'objdeleted'
           try:
               shutil.rmtree(session['tmpdir'],True)
           except Exception as e:
               print e
       #sys.stdout.flush()
       return "deleted"

    
def eval(var1,var2,omc):
   ##run the evaluations in temp directory  ##
   #print 'evalexpression'
   
   x1=var1.split('#')
   y1=var2.split(',')
   x=filter(None,x1)
   y=filter(None,y1)
  
   for i in xrange(len(x)):
      z="\n".join(x[i].splitlines())
      z1 = filter(lambda x: not re.match(r'^\s*$', x), z)
      #z1="".join(x[i].splitlines())
      #simcommand=z1.replace(' ','').startswith('simulate(')and z1.replace(' ','').endswith(')')
      #plotcommand=z1.replace(' ','').startswith('plot(')and z1.replace(' ','').endswith(')')
      #plotparametriccommand=z1.replace(' ','').startswith('plotParametric(')and z1.replace(' ','').endswith(')')
      simcommand=z1.replace(' ','').startswith('simulate(')
      plotcommand=z1.replace(' ','').startswith('plot(')
      plotparametriccommand=z1.replace(' ','').startswith('plotParametric(')

      if (simcommand==True):
        ## look for comments in the string
        s=remove_comments(z1)
        sim=s.replace(' ','').startswith('simulate(')and s.replace(' ','').endswith(')')
        if(sim==True):
		try:
		  s=omc.sendExpression(z1)
		  name=s['resultFile']
		  addmsg=s['messages']
		  if (name!=''):
		     #session['mat'].append(name)
		     mat.append(name)             
		     tempres="".join(['Simulation Success: Temp/',os.path.basename(name)])
		     divcontent=" ".join(['<div id='+y[i]+'>','<b>',str(tempres),'</b>','</div>'])
		  else:
		     error=omc.sendExpression("getErrorString()")
		     finalmsg=error+addmsg
		     divcontent=" ".join(['<div id='+y[i]+' align="justify" >','<b>',str(finalmsg),'</b>','</div>'])
		except:
		   divcontent=" ".join(['<div id='+y[i]+'>','<b>','failed()','</b>','</div>'])         
	
		session['msg'].append(divcontent)

        else:
          try:
            l=omc.sendExpression(z)
          except:
            #l="failed()"
            l=omc.sendExpression(z,parsed=False)            
          divcontent=" ".join(['<div id='+y[i]+'>','<b>',str(l).replace('<','&lt;').replace('>','&gt;'),'</b>','</div>'])
          session['msg'].append(divcontent)
      
      elif (plotparametriccommand==True):
          p=remove_comments(z1)
          pltpar=p.replace(' ','').startswith('plotParametric(')and p.replace(' ','').endswith(')')
          if (pltpar==True):
		  l1=p.replace(' ','')
		  l=l1[0:-1]
		  plotvar=l[15:].replace('{','').replace('}','')
		  divcontent=" ".join(['<div id='+y[i]+'>'])
		  session['msg'].append(divcontent)
		  plotdivid=y[i]
                  #print 'plotparm',plotvar
		  plotgraph(plotvar,plotdivid,omc,"plotParametric")
          else:
		  try:
		    l=omc.sendExpression(z)
		  except:
		    #l="failed()"
		    l=omc.sendExpression(z,parsed=False)            
		  divcontent=" ".join(['<div id='+y[i]+'>','<b>',str(l).replace('<','&lt;').replace('>','&gt;'),'</b>','</div>'])
		  session['msg'].append(divcontent)

      elif (plotcommand==True):
          p=remove_comments(z1)
          plt=p.replace(' ','').startswith('plot(')and p.replace(' ','').endswith(')')
          if(plt==True):
		  l1=p.replace(' ','')
		  l=l1[0:-1]
		  plotvar=l[5:].replace('{','').replace('}','')
		  divcontent=" ".join(['<div id='+y[i]+'>'])
		  session['msg'].append(divcontent)
		  plotdivid=y[i]
		  plotgraph(plotvar,plotdivid,omc,"plot")
          else:
               try:
		    l=omc.sendExpression(z)
	       except:
		    #l="failed()"
		    l=omc.sendExpression(z,parsed=False)            
	       divcontent=" ".join(['<div id='+y[i]+'>','<b>',str(l).replace('<','&lt;').replace('>','&gt;'),'</b>','</div>'])
	       session['msg'].append(divcontent)

      else:
          try:
            l=omc.sendExpression(z)
          except:
            #l="failed()"
            l=omc.sendExpression(z,parsed=False)
            
          divcontent=" ".join(['<div id='+y[i]+'>','<b>',str(l).replace('<','&lt;').replace('>','&gt;'),'</b>','</div>'])
          session['msg'].append(divcontent)
   
   ## delete the process ##
   ##omc.__del__()
   #os.chdir("..")   


def remove_comments(text):
    """ remove c-style comments.
        text: blob of text with comments (can include newlines)
        returns: text with comments removed
    """
    pattern = r"""
                            ##  --------- COMMENT ---------
           /\*              ##  Start of /* ... */ comment
           [^*]*\*+         ##  Non-* followed by 1-or-more *'s
           (                ##
             [^/*][^*]*\*+  ##
           )*               ##  0-or-more things which don't start with /
                            ##    but do end with '*'
           /                ##  End of /* ... */ comment
         |                  ## OR it is a line comment with //
          \s*//.*           ## Single line comment  
         |                  ##  -OR-  various things which aren't comments:
           (                ## 
                            ##  ------ " ... " STRING ------
             "              ##  Start of " ... " string
             (              ##
               \\.          ##  Escaped char
             |              ##  -OR-
               [^"\\]       ##  Non "\ characters
             )*             ##
             "              ##  End of " ... " string
           |                ##  -OR-
                            ##
                            ##  ------ ' ... ' STRING ------
             '              ##  Start of ' ... ' string
             (              ##
               \\.          ##  Escaped char
             |              ##  -OR-
               [^'\\]       ##  Non '\ characters
             )*             ##
             '              ##  End of ' ... ' string
           |                ##  -OR-
                            ##
                            ##  ------ ANYTHING ELSE -------
             .              ##  Anything other char
             [^/"'\\]*      ##  Chars which doesn't start a comment, string
           )                ##    or escape
    """

    regex = re.compile(pattern, re.VERBOSE|re.MULTILINE|re.DOTALL)
    noncomments = [m.group(2) for m in regex.finditer(text) if m.group(2)]

    return "".join(noncomments)

   
def plotgraph(plotvar,divid,omc,command):
  
  ## Function to handle plotting in browser ##
  if (len(mat)!=0):
     res=mat[-1]
     try:
       if(command=="plotParametric"):
           readResult = omc.sendExpression("readSimulationResult(\"" + os.path.basename(res) + "\",{" + plotvar + "})")
           scaledxrange="["+str(min(readResult[0]))+","+str(max(readResult[0]))+"]"
           plotlabels=[]
       else:
           readResult = omc.sendExpression("readSimulationResult(\"" + os.path.basename(res) + "\",{time," + plotvar + "})")
           plotlabels=['Time']
   
       omc.sendExpression("closeSimulationResultFile()")

       exp='(\s?,\s?)(?=[^\[]*\])|(\s?,\s?)(?=[^\(]*\))'
       #print 'inside_plot1'
       subexp=re.sub(exp,'$#',plotvar)
       plotvalsplit=subexp.split(',')
       #print plotvalsplit
       for z in xrange(len(plotvalsplit)):
           val= plotvalsplit[z].replace('$#',',')
           plotlabels.append(val)
       #print plotlabels  
       plotlabel1=[x.encode('UTF8') for x in plotlabels]
       
       plots=[]
       for i in xrange(len(readResult)):   
         x=readResult[i]
         d=[]
         for z in xrange(len(x)):
            tu=x[z]
            d.append((tu,))
         plots.append(d)            
       n=numpy.array(plots)
       numpy.set_printoptions(threshold='nan')
       dygraph_array= repr(numpy.hstack(n)).replace('array',' ').replace('(' ,' ').replace(')' ,' ')
       if(command=="plotParametric"):
           dygraphoptions=" ".join(['{', 'legend:"always",','dateWindow:',scaledxrange,',','labels:',str(plotlabel1),'}'])
       else:
           dygraphoptions=" ".join(['{', 'legend:"always",','labels:',str(plotlabel1),'}'])

       data="".join(['<script type="text/javascript"> g = new Dygraph(document.getElementById('+'"'+str(divid)+'"'+'),',str(dygraph_array),',',dygraphoptions,')','</script>']) 
       divcontent="\n".join([str(data),"</div>"])
       session['msg'].append(divcontent)
     except:
       error=omc.sendExpression("getErrorString()")
       divcontent="".join(['<b>',error,'</b>',"</div>"])
       session['msg'].append(divcontent)
      
  else:
     divcontent="".join(['<b>','No result File Generated','</b>',"</div>"])
     session['msg'].append(divcontent)
    
    

if __name__ == '__main__':
    #app.run(debug=True,use_reloader=True)
    app.run(host='0.0.0.0')
