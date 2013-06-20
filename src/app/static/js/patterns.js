    function buildPatternCombo(pattern_uri, pattern_template, pattern_text, type)
    {
        
        var editor_div_id; 
        if (type =="i") {
                editor_div_id =  "#editor";
        } else
                editor_div_id =  "#editorE";
        
        
        var pattern_values = $.localStorage('patternvalues');
        
        // var default_datatype_suffix = '^^<http://www.w3.org/2001/XMLSchema#string>';
        
        var needle = '{}';
        var re = new RegExp(needle, 'g');
        
        
        // Replace the {} in pattern_template with input fields, create a div, and add it to the #editor div
        pattern_html = pattern_template.replace(re, '<input type="hidden" class="entry"></input><a class="add"><i class="icon-plus"></i></a>');
    
        var close = $('<a href="#" class="close" data-dismiss="alert"><i class="icon-remove"></i></a>&nbsp;');
        var p_eval_div = $('<div class="pattern-and-eval"></div>');
        p_eval_div.append(close);
        
        var pattern_div = $('<div class="pattern alert alert-info" value="'+ pattern_uri +'" type="'+type+'">'
                            +pattern_html
                            +'</div>'
                            );
        
        
        var evaluation_div = $('<div class="eval"><small><form class="form-horizontal">'
                                 +'<label class="radio inline"><input type="radio" name="ok" />Ok</label>'
                                 +'<label class="radio inline"><input type="radio" name="incomplete" checked/>Incomplete</label>'
                                + '</form></small></div>');
  
        // Build some examples (i.e. show instances of the pattern selected)
        
        $.getJSON('/patterninstances',{'uri': pattern_uri}, function(data){
            console.log(data.instances);
            if (data.instances.length != 0) {
                var examples_close = $('<a href="#" class="close"><i class="icon-remove"></i></a>');
                var examples_div = $('<div class="alert alert-warning examples"></div>').append(examples_close).hide();
                 
                examples_close.click(function(event){
                    examples_div.toggle();
                })
                 
                
                $.each(data.instances, function (key, value){
                    examples_div.append('<div class="small">'+value+'</div>');
                });
                
                var help = $('<a href="#" class="close"><i class="icon-question-sign"></i></a>');
                help.click(function(event) {
                    examples_div.toggle();
                });
                
                close.after(help);
                

                $(editor_div_id).append(examples_div);
            }
        });
        
        p_eval_div.append(pattern_div);
        p_eval_div.append(evaluation_div);
        $(editor_div_id).append(p_eval_div);
        
        
        

 
     
          
        // This is the Select2 stuff for the Concepts
        
        var select2_initialization = {
            data : pattern_values,
            placeholder: 'concept or value',
            width: '200px',
            multiple: false,
            createSearchChoice:function(term, data) {
                if ($(data).filter(function() {
                                        return this.text.localeCompare(term)===0;
                                    }).length===0) {
                    
                    new_value = {'id': '"'+ term +'"', 'text': term};
                    return new_value;
                }
            }
        }
 
        //$(editor_div_id + " input").select2(select2_initialization);
        $(editor_div_id + " .entry").select2(select2_initialization);       
      
     
        
        $(editor_div_id + " .add").click(function(event) {
            var new_input = $('<input type="hidden"></input>');
            $(this).before(new_input);
            new_input.select2(select2_initialization);
        });
        
        //$(".radio").buttonset(); 
    
        }
