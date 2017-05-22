$(document).ready(function(){
        // hide the progress bar when the document loads
        $("#progressbar").hide();
        var focusid=''
        var countid=''
        var count = 0;
        var value = '';
        
        
        function guid() {
             function s4() {
               return Math.floor((1 + Math.random()) * 0x10000)
              .toString(16)
              .substring(1);
             }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
           }
        
        $( window ).load(function() {
            //alert("loading")
          console.log('loading');
          var uuid = guid();
          //console.log(value);
          value=uuid        
          //console.log(uuid);  
          var url = '/createsession'
           $.ajax(
             {
              url: url, 
              type: 'POST',
              data:{sid:uuid},        
              success: function(result){
                          console.log('success');
              //alert(result)
                 }                  
                     }); 
            });
        $( window ).bind("beforeunload",function() {
           console.log('unloading');
           var url = '/deletesession'
           $.ajax(
             {
              url: url, 
              async: false,
              type: 'POST',
              data:{sid:value},              
              success: function(result){
                          console.log('success');
              //alert(result)
                 }                  
                     }); 

        });
              
       $('textarea').each(function(){
       $(this).textareaHighlighter({
               matches: [
                 {
                'match': ['for','end','equation','model','class','der',
                          'algorithm','and','annotation','assert','block','if',
                          'connect','connector','constant','discrete','else',
                          'elseif','elsewhen','encapsulated','enumeration','for',
                          'extends','external','false','final','flow','function',
                          'in','inner','input','loop','not','or','outer','output',
                          'package','parameter','partial','protected','public',
                          'record','redeclare','replaceable','terminate','then',
                          'true','type','when','while','within'], // will check for this matches
                'matchClass': 'match' // on matched text this class will be added
                    },
                ]
                   });
            });  
        // code to add textarea, checkbox and div dynamically
         /*        
         $('#addtextcells').click(function(){          
           var newtextarea= $('<div id="check'+count+'row" class="row"> </div> <div class="col-sm-6" style="background-color:LightYellow ;"> <textarea class=target rows= 1 id="check'+count+"textarea"+'" > </textarea> <div id="check'+count+"div"+'"> </div> </div></div>').on('click',function(){
              countid='check'+count 
              focusid=this 
              $('textarea').click(function (){
              //focusid=this
              applyhighlight(this)
              }); 
              });              
            $('#cells').append(newtextarea)
            count++              
          });*/
        
         $("textarea").click(function() {
             //alert(this.id);
           focusid=this
          // applyhighlight(this)
           $(this).focus();
           //var current= $(this).focus().attr("id");
          });
        
        
        $('#addtextcells').click(function(){          
           var newtextarea='<div id="check'+count+'row" class="row"> <textarea class=target rows= 1 id="check'+count+"textarea"+'" > </textarea> <div id="check'+count+"div"+'"> </div> </div>'
              countid='check'+count 
              //focusid=this 
              $('#cells').append(newtextarea)
            count++              
          });       
       function applyhighlight(object)   
        {
          $(object).textareaHighlighter({
               matches: [
                 {
                'match': ['for','end','equation','model','class','der',
                          'algorithm','and','annotation','assert','block','if',
                          'connect','connector','constant','discrete','else',
                          'elseif','elsewhen','encapsulated','enumeration','for',
                          'extends','external','false','final','flow','function',
                          'in','inner','input','loop','not','or','outer','output',
                          'package','parameter','partial','protected','public',
                          'record','redeclare','replaceable','terminate','then',
                          'true','type','when','while','within'], // will check for this matches
                'matchClass': 'match' // on matched text this class will be added
                    },
                ]
                   });
          }        
         
         $('#evaluateall').click(function(){ 
            var divid=[]
            var valuesArray = $('textarea').map( function() {
              var textareaid=this.id
              var newdivid=textareaid.replace("textarea", "div");
              divid.push(newdivid);                
              var textcontents="#"+textareaid;
              return $(textcontents).val()
             }).get().join("#"); 
             
             var divlisttostring=divid.toString();
             //alert(valuesArray)
             if (divid.length != 0)
              {
              $("#progressbar").show();           
              var url = '/evalexpression'
              $.ajax(
               {
               url: url, 
               data:{input:valuesArray,output:divlisttostring,sid:value},
               type: 'POST',              
               success: function(result){
               $("#progressbar").hide();
               //alert(result)
               alert("Ok")
               if (result!="failed")
                {                    
               var $response=$(result);
               for (var i = 0; i < divid.length; i++) 
                  {
                 var loopid="#"+divid[i]
                 //alert(loopid)
                 //var oneval = $response.filter(loopid).text();
                 var oneval = $response.filter(loopid);
                 $(loopid).html(oneval);
                 }
                   } 
                 else
                 {
                  alert("Could not be evaluated due to unknown reasons")
                 }  
                   }                 
                     });                           
             }
             else
             {
               alert("No Cells Selected To Evaluate")
              } 

        });         
         // code to evaluate modelica codes        
         $('#evaluate').click(function(){
          //alert(value);
          var divid=[]
          var valuesarray=[]
          if (focusid!='')
          {
         
            var textareaid=focusid.id
            var textcontents="#"+textareaid;
            var textval=$(textcontents).val()+"#";  
            valuesarray.push(textval)
            var newdivid=textareaid.replace("textarea", "div");
            divid.push(newdivid);
            var divlisttostring=divid.toString();
            var valuesArray=valuesarray.toString();
            //alert(valuesArray)
            if (divid.length != 0)
             {
              $("#progressbar").show();           
              var url = '/evalexpression'
              $.ajax(
               {
               url: url, 
               data:{input:valuesArray,output:divlisttostring,sid:value},
               type: 'POST',              
               success: function(result){
               $("#progressbar").hide();
               alert("Ok")
               if (result!="failed")
                {                       
               var $response=$(result);
               for (var i = 0; i < divid.length; i++) 
                  {
                 var loopid="#"+divid[i]
                 //alert(loopid)
                 //var onevaltext = $response.filter(loopid).text();
                 //alert(onevaltext)
                 //console.log(onevaltext);  
                 var oneval = $response.filter(loopid);
                 $(loopid).html(oneval);
                 }
                 }
                 else
                 {
                  alert("Could not be evaluated due to unknown reasons")
               }       
                 }
                                     
                     });                           
             }
             else
             {
               alert("No Cells Selected To Evaluate")
              }
           }
          else
            {
             alert("Nothing to evaluate, Add cells first to evaluate")
               }            
              });
         
         $('#inserttextcells').click(function(){
            //alert(focusid.id)
            if (focusid!='')
             {
            var divrow="#"+focusid.id.replace('textarea','row')
            //alert(divrow)
            var newtextareainsert='<div id="check'+count+'row" class="row"> <textarea class=target rows= 1 id="check'+count+"textarea"+'" > </textarea> <div id="check'+count+"div"+'"> </div> </div>'
              countid='check'+count 
              $(divrow).after(newtextareainsert);
            count++    
               }
            else
              {
               alert("No cells selected to insert between")
                }              
          });  
             
                
         // code to save the document
           $('#save').click(function(){
                window.print();     
           });
         
         // code to delete cells       
         $('#deletetextcells').click(function(){
          if (focusid!='')
             {
            var rowid="#"+focusid.id.replace('textarea','row')
            $(rowid).remove();
                }
           else
             {
              alert("No Cells Selected To Delete")
                 }             
               });
    });
