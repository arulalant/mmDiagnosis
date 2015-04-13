/*
.. module:: diagnosis.js
   :synopsis: This script will be imported in the 'index.html' for the 
              purpose of usability events like click, change, show and hide.
              
              Using 'diagnosis.css', we used showCls and hideCls to user's 
              view purpose.
              
JQuery Version : 1.7

Version : 0.1a

Written by: Arulalan.T

Date: 16.11.2011
*/

var modelName = "";
var premodelName = "";
var premodel = "";
var preprocess = "";
var preyearPid = "";
var preyear = "";
var premonseasonPid = "";
var premonseason = "";
var preregionhrPid = "";
var preplotPid = "";
var preregionhr = "";
var pretablePid = "";
var preplot = "";
var tableid = "";

$(document).ready(function(){
    // reset all the select (combo boxes) into null value once page as reloaded
    $("select.selectCls option[selected]").removeAttr("selected");
    $("select.selectCls option[value='']").attr("selected", "selected");
    
    $(".model").live("click", function(){        
        $("#go").css('visibility','visible');
        modelName = $(this).val();
        $('#' +  tableid).addClass('hideCls');        
        $('#' + pretablePid).addClass('hideCls');                       
    });   
    
    $("#go").live("click", function(){
         // reset all the select (combo boxes) into null value once model changed
         $("select.selectCls option[selected]").removeAttr("selected");
         $("select.selectCls option[value='']").attr("selected", "selected");           
         var modelid = modelName + "_Select";
              
         if (premodelName){
             if (modelName != premodelName){
                // hide the whole class
                $('.' + premodelName + 'Cls').addClass('hideCls');      
                if ($("." + modelName + 'Cls').hasClass('hideCls')){
                    // show the selected div element
                    $("." + modelName + 'Cls').removeClass('hideCls');
                }
             }
         }
         premodelName = modelName;
         // show the model process select box
         $("#" + modelid).show();
         // show the Type of plot text p element           
         $("#P" + modelid).show();
         // set the position of the process select box      
         $("#" + modelid).css({"position":"absolute", "top":"40px"});
         
         $("#" + modelid).change(function(){
            var process = $(this).val();
            var YearPid = modelName + "_" + process;
            if(process){
                // selected some value
                if (process != preprocess){
                    // hide the whole class                   
                    $('.' + preyearPid  + 'Cls').addClass('hideCls');                    
                    if ($('.' + YearPid + 'Cls').hasClass('hideCls')){
                        // show the selected div element
                        $('.' + YearPid + 'Cls').removeClass('hideCls');
                        // hide the sub elements of the above element
                        $('.' + premonseasonPid + 'Cls').addClass('hideCls');                    
                    }
                }                      
            }          
            else{
                // selected default empty option
                // hide the whole class                  
                $('.' + modelid  + 'Cls').addClass('hideCls');
            }
                        
            preyearPid = YearPid;            
            preprocess = process;
            var yearid = YearPid + "_Select";
            // reset year the select (combo boxes) into null value 
            $("select#"+ yearid +" option[selected]").removeAttr("selected");
            $("select#"+ yearid +" option[value='']").attr("selected", "selected");   
            // show the year select box          
            $("#" + yearid).show();                   
            // show the Year text p element            
            $("#P" + yearid).show();
            // set the position of the year select box 
            $("#" + yearid).css({"position":"absolute", "top":"80px"});
            
            $("#" + yearid).change(function(){
                var year = $(this).val();                
                var monseasonPid = YearPid + '_' + year;
                if(year){
                    // selected some value
                    if (year != preyear){
                        // hide the whole class
                        $('.' + premonseasonPid + 'Cls').addClass('hideCls');
                        if ($('.' + monseasonPid + 'Cls').hasClass('hideCls')){
                            // show the selected div element
                            $('.' + monseasonPid + 'Cls').removeClass('hideCls');
                            // hide the sub elements of the above element
                            $('.' + preregionhrPid + 'Cls').addClass('hideCls');                    
                        }
                    }
                }
                else{
                    // selected default empty option
                    // hide the whole class                                   
                    $('.' + YearPid + '_' + preyear  + 'Cls').addClass('hideCls');
                }
                premonseasonPid = monseasonPid;
                preyear = year;
                var monseasonid = monseasonPid + '_Select'
                // reset year the select (combo boxes) into null value 
                $("select#"+ monseasonid +" option[selected]").removeAttr("selected");
                $("select#"+ monseasonid +" option[value='']").attr("selected", "selected"); 
                // show the monseason select box  
                $("#" + monseasonid).show();
                // show the Time period text p element            
                $("#P" + monseasonid).show();
                // set the position of the monseason select box 
                $("#" + monseasonid).css({"position":"absolute", "top":"120px"});
                
                $("#" + monseasonid).change(function(){
                     var monseason = $(this).val();   
                     var regionhrPid =  monseasonPid + '_' + monseason;
                     if(monseason){
                        // selected some value
                        if (monseason != premonseason){
                            // hide the whole class
                            $('.' + preregionhrPid + 'Cls').addClass('hideCls');
                            if ($('.' + regionhrPid + 'Cls').hasClass('hideCls')){
                                // show the selected div element
                                $('.' + regionhrPid + 'Cls').removeClass('hideCls');
                                // hide the sub elements of the above element
                                $('.' +  preplotPid + 'Cls').addClass('hideCls');                      
                            }
                        }
                    }
                    else{
                        // selected default empty option
                        // hide the whole class                  
                        $('.' + monseasonid  + 'Cls').addClass('hideCls');
                    }
                    preregionhrPid = regionhrPid;
                    premonseason = monseason;
                     
                    var regionhrid = regionhrPid + '_Select';
                    // reset regionhrid the select (combo boxes) into null value 
                    $("select#"+ regionhrid +" option[selected]").removeAttr("selected");
                    $("select#"+ regionhrid +" option[value='']").attr("selected", "selected");  
                    // show the regionhr select box  
                    $("#" + regionhrid).show();  
                    // show the Forecast Hour text p element            
                    $("#P" + regionhrid).show();
                    // set the position of the regionhr select box 
                    $("#" + regionhrid).css({"position":"absolute", "top":"160px"});                   
                     
                    $("#" + regionhrid).change(function(){
                        var regionhr = $(this).val();
                        var thisname = $(this).attr('name');
                        var plotPid =  regionhrPid + '_' + regionhr;
                        if (thisname == "plot"){
                            var endname = '_Table';                            
                            var id = '#'
                        }
                        else{
                            var endname = 'Cls';   
                            var id = '.'
                        }
                        if(regionhr){                            
                            // selected some value
                            if (regionhr != preregionhr){                                
                                // hide the whole class
                                $(id + preplotPid + endname).addClass('hideCls');
                                if ($(id + plotPid + endname).hasClass('hideCls')){
                                    // show the selected div element
                                    $(id + plotPid + endname).removeClass('hideCls');
                                    // hide the sub elements of the above element
                                    $(id +  pretablePid + endname).addClass('hideCls');       
                                    $('#' +  tableid).addClass('hideCls');
                                }
                            }
                        }
                        else{
                            // selected default empty option
                            // hide the whole class                                                                         
                            $('.' + regionhrid  + 'Cls').addClass('hideCls');                            
                        }
                        preplotPid = plotPid;
                        preregionhr = regionhr;                            
                        var plotid = plotPid + '_Select';  
                                               
                        if($(this).attr("name") == "plot"){                                           
                            tableid = plotPid + '_Table';
                            // show the plot table                                              
                            $("#" + tableid).show();
                        }
                        else{
                            // reset plotid the select (combo boxes) into null value 
                            $("select#"+ plotid +" option[selected]").removeAttr("selected");
                            $("select#"+ plotid +" option[value='']").attr("selected", "selected"); 
                             // show the plot select box  
                            $("#" + plotid).show();
                            // show the Plots text p element            
                            $("#P" + plotid).show();
                            // set the position of the plot select box 
                            $("#" + plotid).css({"position":"absolute", "top":"200px"});  
                            
                            $("#" + plotid).change(function(){                                
                                var plot = $(this).val();                                
                                var tablePid = plotPid + '_' + plot + '_Table';                       
                                if(plot){
                                    // selected some value
                                    if (plot != preplot){
                                        // hide the whole class
                                        $('#' + pretablePid).addClass('hideCls');
                                        if ($('#' + tablePid).hasClass('hideCls')){
                                            // show the selected div element
                                            $('#' + tablePid).removeClass('hideCls');                                            
                                        }
                                    }
                                }
                                else{
                                    // selected default empty option
                                    // hide the whole class                                                        
                                    $('.' + plotid  + 'Cls').addClass('hideCls');
                                }
                                pretablePid = tablePid;
                                preplot = plot;
                                // show the plot table                                                                             
                                $("#" + tablePid).show();
                            });
                        }
                        
                        $(".imgCls").mouseover(function(){                            
                            imglink = $(this).attr('href');
                            imgpre = '<img src ="' + imglink + '", width = "640", height = "480"/>'
                            preview = '<p><b>Preview</b></p>'                           
                            $("#preview").html(preview + imgpre);
                        });
                       
                       $(".imgCls").mouseout(function(){                                                        
                            $("#preview").html('<img src="css/dummy.png" width="180", height="180"/>');
                        });
                                           
    
                     });
                     
                });
                
            });
            
        });   
   
   });    
    
});
