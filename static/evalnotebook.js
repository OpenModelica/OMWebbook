$(document).ready(function () {
  $.getScript("../jquery.key.js", function () {
    //alert("Script loaded.");

    /* evaluate cells using keys shift+enter */
    $.key("shift+return", function () {
      evaluate()
    });

    /* evaluate all cells using keys shift+ctrl */
    $.key("shift+ctrl", function () {
      evaluateall()
    });
  });

  $("#progressbar").hide();
  count = 0;
  var editorinstance = []
  var editorid = ''
  var value = '';

  /* function to generate unique id for each session */
  function guid() {
    function s4() {
      return Math.floor((1 + Math.random()) * 0x10000)
        .toString(16)
        .substring(1);
    }
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
  }


  /* create a unique omc session object */
  $(window).on('load', function() {
    //alert("loading")
    //console.log('loading');
    var uuid = guid();
    //console.log(value);
    value = uuid
    //console.log(uuid);
    var url = '/createsession'
    $.ajax(
      {
        url: url,
        type: 'POST',
        data: { sid: uuid },
        success: function (result) {
          //console.log('success');
          //alert(result)
        }
      });
  });

  /* delete the omc session */
  $(window).bind("beforeunload", function () {
    console.log('unloading');
    var url = '/deletesession'
    $.ajax(
      {
        url: url,
        async: false,
        type: 'POST',
        data: { sid: value },
        success: function (result) {
          console.log('success');
          //alert(result)
        }
      });

  });

  /* Translate html textarea into codemirror textarea editor */
  $('textarea').each(function () {
    var textareaid = this.id
    var editor = CodeMirror.fromTextArea(document.getElementById(textareaid), {
      lineNumbers: true,
      mode: "text/x-modelica",
      autoRefresh: true,
      extraKeys: {
        "Shift-Enter": onNewLine
      },
      viewportMargin: Infinity
    });
    editorinstance.push(editor)

    /* handle click event for selecting a cells */
    editor.on('mousedown', function () {
      editorid = editor
    });

    /* prevent default functionality when shift+enter pressed */
    function onNewLine(e) {
      if ((e.keyCode == 10 || e.keyCode == 13)) {
        e.preventDefault();
      }
    }

  });

  /* function to evaluate single cells */
  function evaluate() {
    var divid = []
    var valuesarray = []
    //alert(editorid.getValue())
    //alert(editorid.getTextArea().id)
    if (editorid != '') {
      var textareaid = editorid.getTextArea().id
      var textval = editorid.getValue() + "#";
      valuesarray.push(textval)
      var newdivid = textareaid.replace("textarea", "div");
      divid.push(newdivid);
      var divlisttostring = divid.toString();
      var valuesArray = valuesarray.toString();
      //alert(valuesArray)
      if (divid.length != 0) {
        $("#progressbar").show();
        var url = '/evalexpression'
        $.ajax(
          {
            url: url,
            data: { input: valuesArray, output: divlisttostring, sid: value },
            type: 'POST',
            success: function (result) {
              $("#progressbar").hide();
              //alert("Ok")
              if (result != "failed") {
                var $response = $(result);
                for (var i = 0; i < divid.length; i++) {
                  var loopid = "#" + divid[i]
                  //alert(loopid)
                  //var onevaltext = $response.filter(loopid).text();
                  //alert(onevaltext)
                  //console.log(onevaltext);
                  var oneval = $response.filter(loopid);
                  $(loopid).html(oneval);
                }
              }
              else {
                alert("Could not be evaluated due to unknown reasons")
              }
            }

          });
      }
      else {
        alert("No Cells Selected To Evaluate")
      }
    }
    else {
      alert("Nothing to evaluate, Add cells first to evaluate")
    }

  }

  /*function to evaluate all cells in document */
  function evaluateall() {
    var divid = []
    var tempArray = []
    for (var i = 0; i < editorinstance.length; i++) {
      var inst = editorinstance[i]
      var textareaid = inst.getTextArea().id
      var newdivid = textareaid.replace("textarea", "div");
      divid.push(newdivid);
      //alert(inst.getTextArea().id)
      //alert(inst.getValue())
      txtareavalue = inst.getValue()
      tempArray.push(txtareavalue)
      //alert(txtareavalue)
    }
    var valuesArray = tempArray.join('#')
    //alert(valuesArray)
    var divlisttostring = divid.toString();
    //alert(valuesArray)
    if (divid.length != 0) {
      $("#progressbar").show();
      var url = '/evalexpression'
      $.ajax(
        {
          url: url,
          data: { input: valuesArray, output: divlisttostring, sid: value },
          type: 'POST',
          success: function (result) {
            $("#progressbar").hide();
            //alert(result)
            //alert("Ok")
            if (result != "failed") {
              var $response = $(result);
              for (var i = 0; i < divid.length; i++) {
                var loopid = "#" + divid[i]
                //alert(loopid)
                //var oneval = $response.filter(loopid).text();
                var oneval = $response.filter(loopid);
                $(loopid).html(oneval);
              }
            }
            else {
              alert("Could not be evaluated due to unknown reasons")
            }
          }
        });
    }
    else {
      alert("No Cells Selected To Evaluate")
    }

  }
  /* evaluate single cells */
  $('#evaluate').click(function () {
    //alert(value);
    evaluate()
  });

  /* evaluate all cells */
  $('#evaluateall').click(function () {
    //alert(editorinstance)
    evaluateall()
  });

});
