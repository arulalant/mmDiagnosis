/*
.. module:: diagnosis.js
   :synopsis: This script will be imported in the 'index.html' for the 
              purpose of usability events like click, change, show/hide and 
              it should generate the select boxes and tables dynamically 
              by reading the diangosis.json file.
              
              Using 'diagnosis.css' we made alignments.
              
JQuery Version : 1.7

Version : 0.2a

Written by: Arulalan.T

Date: 07.02.2012
*/
 
/* Initialize global variables */
process = "";
preprocess = "";
year = "";
preyear = "";
premodelName = "";
modelName = ""; 
preperiod = "";
period = "";  
prehrReg = "";
hrReg = "";
selectorObjList = "";
presubperiod = "";
subperiod = "";
hrRegExcept = "";

jQuery(document).ready(function($) {


//$("[title]").tooltip();

/* Make all the select boxes are selected the default option, when reload the web page */
$("select.selectCls option[selected]").removeAttr("selected");
$("select.selectCls option[value='']").attr("selected", "selected");
    

$.ajaxSetup({'beforeSend': function(xhr){
    if (xhr.overrideMimeType)
        xhr.overrideMimeType("text/plain");
    }
});

    /* Open the short_names_abbreviation.json file & make available it as var data */
    var short_names_abb = null;
    $.getJSON("/js/short_names_abbreviation.json", function(json) {
      short_names_abb = json["names"];
    });
    
    /* Function to access the short_names_abb var data, return the proper value */
    getAbb = function(key){
        var value = '';
        key = key.toUpperCase();
        if (key in short_names_abb){
            value = short_names_abb[key];
        }
        return value;
    }
    
    /* Open the diagnosis.json */
    $.getJSON("/js/diagnosis.json", function(data){  //alert('loaded success');
        data = data['model'];
        
        getPartialJsonObject = function(jsonData, listOfObjects){            
            /* Get the partial data object from the data which is loaded from 
               the diagnosis.json or it may be even partial data object itself.
                
               Args:
                 jsonData - json full data or partial data
                 listOfObjects - list contains the objects to walk through
                        the passed jsonData to split/partition the jsonData */
            var index, obj;            
            for (index in listOfObjects){
                obj = listOfObjects[index];                
                jsonData = jsonData[obj];                                                
            }
            return jsonData;
        }
   
        getValue = function(listOfObjects, expect){
            /*  */
            var tmpObj = getPartialJsonObject(data, listOfObjects);
            var keys = new Array(); 
                        
            if (expect == "array"){
                $.each(tmpObj, function(index, item) {                
                    for (var key in item){
                        keys.push(key);                
                    }            
                });
            }
            else if (expect == "dictionary"){
                for (var key in tmpObj){
                        keys.push(key);                
                    }
            }
            else{
                alert("Wrong input");
            }
            return keys;

        }
      
      getSortedHeaders = function(tmpObj){
        var rowHeader = new Array(); 
        var colHeader = new Array();             
        // collecting the row and column headers
        $.each(tmpObj, function(cindex, citem){         
            for (var ckey in citem){
                colHeader.push(ckey);                                    
            }                         
            $.each(citem[ckey], function(rindex, ritem){                    
                for (var rkey in ritem){
                    rowHeader.push(rkey); 
                }                    
            });                                
        });          
        // make unique of colHeader            
        rowHeader = rowHeader.sort();
        rowHeader = $.unique(rowHeader).sort(); // unique has bug.
        // CAUTION : Dont sort the colHeader.
        return [rowHeader, colHeader];
    }
            
    genTable = function(id, attachId, listOfObjects, exceptList){
                
        if(typeof(exceptList)==='undefined') exceptList = '';
        
        var tableHeaderThValues = new Array();
        var tmpObj = getPartialJsonObject(data, listOfObjects);

        var headersList = getSortedHeaders(tmpObj);            
        var rowHeader = headersList[0]; 
        var colHeader = headersList[1]; 
        
        var $table = $("<table>").attr({id : id, 'class': 'tableCls', border: 1});
        
        var $thead = $("<thead>");
        $thead.append($("<th>Variables</th><th>Level</th>"));
        
        var $tbody = $("<tbody>");
        
        $table.append($thead);
        $table.append($tbody);
        $(attachId).append($table); 
                    
        if (exceptList){
            for (var i in exceptList){ 
            var val = exceptList[i];
            var valIndex = $.inArray(val, colHeader);
            if (valIndex > -1)
                // remove element from the js array
                colHeader.splice(valIndex, 1);
                 
            }                
        }
        
        var tmpObjColHeader = new Array();
        $.each(tmpObj, function(cindex, citem){
            for (var val in citem)
                tmpObjColHeader.push(val);
                
        });    
        
        for (var rindex in rowHeader){
            /* Outer variable name loop. i.e. Here we make single 
                variable <tr> tag with rowspan val of 2 */ 
            rval = rowHeader[rindex]; 
            if(rindex % 2){
                var modCls = 'evenCls';
            }
            else{
                var modCls = 'oddCls';
            }
            var rtitle = getAbb(rval);
            var $outTr = $tbody.append($("<tr>").attr({'id': rval + '_row',
                                                       'class': modCls})
                                             .append($("<th>")
                                                     .attr({id: rval + '_rowspan',
                                                            rowspan: 2,
                                                            'class': 'rowspanCls',
                                                            'title': rtitle})
                                                     .text(rval)
                                                     )
                                                    );
            var flag = true;
            
            for (var cindex in colHeader){
                /* Month or Season or Hours or Region loop */
                var row = colHeader[cindex]; 

                if ($.inArray(row, tableHeaderThValues) < 0){                
                    $thead.append($("<th>").attr('class', 'headTHCls').append(row.substr(0,4))); 
                    tableHeaderThValues.push(row);                        
                }
                
                citem = tmpObj[tmpObjColHeader.indexOf(row)];
               
                ritem = citem[row][rindex]; 
                /* Outer variable object comes here, to access the 
                   primary and secondary objects */
                 
                var path = ritem[rval].path;  
                var primary = ritem[rval].primary;
                var pcount = true;
                for (var cval in primary){ 
                    /* loop through variable's primary object keys.
                       i.e. loop through only the primary levels or 
                       threshold keys.
                       Here we make <td> value with level and <td> 
                       with image link */                 
                    var tmp = primary[cval];
                    var colVal = tmp[0];
                    var imglink = path + '/' + tmp[1];                    
                    var $img = $("<img>").attr({src: 'css/thumbnail1.png'});
                    var $link = $("<a>").attr({href: imglink,
                                               target: '_blank',
                                               'class': 'imgCls'});                    
                    $link.append($img);
                    var $_row = $("#" + id + " > tbody > tr[id='" + rval + "_row']");
                    var ctitle = getAbb(colVal);
                    var mtitle = getAbb("More");
                    if(flag){
                        /* Add the level/threshold value of first row 
                            and second column of the table */
                        flag = false;                        
                        $_row.append($("<td>").attr({'class': 'levelCls',
                                                     'title': ctitle}).append(colVal));
                    }
                    if (pcount){
                        /* Add the image link for all the 
                           months/seasons/hours/etc of first row 
                           of the table */
                        pcount = false;
                        $_row.append($("<td>").attr('class','linkCls cellCls').append($link));  
                    }
                    else{
                        /* Second rows falls here */
                        var trId = rval + '_moreRow'; //'_' + cval.replace('.', '_');
                        var $_tr = $("#" + id + " > tbody > tr[id='" + trId + "']");
                        if (!$_tr.length){
                            /* Add level/threshold value in the 2nd row,
                              2nd column. In this <td>, we are spliting 
                              into rowspan of 1, to add the 'More' 
                              link to view the secondary objects level
                              images */
                            var $tr = $("<tr>").attr({'id': trId,
                                                      'class': modCls});                 
                            //var $tr = $("<tr>").attr('id', rval + '_moreRow');
                            $tr.append($("<th>").attr({'rowspan': 1,
                                                       'class': 'rowCls',
                                                       'title': ctitle})
                                                .text(colVal)
                                                .append($("<td>")
                                                .attr({id: rval+"_more",
                                                     'class': 'moreCls',
                                                     'title': mtitle})
                                                .append("(+) More")));
                                                //.click(moreFn)));
                            /* Add the image link <td> of 2nd row,
                              3rd column */
                            $tr.append($("<td>").attr('class','linkCls cellCls').append($link));
                            $outTr.append($tr);                                                
                        }
                        else{
                            /*Add the image link <td> of 2nd row, 
                            rest of the columns */
                            $_tr.append($("<td>").attr('class','linkCls cellCls').append($link));
                        }
                    }
                }                
           
        } 
        
    }
                
        genSecondaryOfTable = function(id, selectorObjList, variable, exceptList){                    
                   /* Get the row span value */
                                     
                                      
            if(typeof(exceptList)==='undefined') exceptList = '';

          
           var $outTr = $("#" + id + "  tbody  tr[id='" + variable + "_moreRow']");

           var modCls = $outTr.attr('class');
           var $secondaryTable = $("<table>").attr({id: variable + '_secondaryTable'}).append("<body>");
                                
           var $rowspan = $("#" + id + " > tbody > tr > th[id='" + variable + "_rowspan"+ "']");                   
           var rowSpanCount = $rowspan.attr('rowspan');
           $rowspan.attr('rowspan', ++rowSpanCount);
                              
           var lefPos = $outTr.find("th").position().left;
           
           
           var $div = $("<div>").attr({id: variable + '_SecondaryDiv',
                                       'class': modCls})
                                .css({position: "absolute", 
                                      left: lefPos + "px"});


            $outTr.after($("<tr>").attr({id: variable + '_dummyTr',
                                         'class': modCls})
                                    .append($("<div>")
                                    .attr({id: variable + '_dummyDiv'})));

            $outTr.after($div.append($secondaryTable));
           
           var tmpObj = getPartialJsonObject(data, selectorObjList);
            var headersList = getSortedHeaders(tmpObj);            
            var rowHeader = headersList[0]; 
            var colHeader = headersList[1];
            var rindex = rowHeader.indexOf(variable);
                              
           
           if (exceptList){
            for (var i in exceptList){ 
                var val = exceptList[i];
                var valIndex = $.inArray(val, colHeader);
                if (valIndex > -1)
                    // remove element from the js array
                    colHeader.splice(valIndex, 1);                             
                }                   
            }
           
           var tmpObjColHeader = new Array();
            $.each(tmpObj, function(cindex, citem){
                for (var val in citem)
                    tmpObjColHeader.push(val);
                    
            }); 
                   
                   
            for (var cindex in colHeader){
                /* Month or Season or Hours or Region loop */
                var row = colHeader[cindex];        
                
                if (exceptList){ 
                    if ($.inArray(row, exceptList) > -1)
                        // return false is equals to continue statement;
                        return false;

                }
                citem = tmpObj[tmpObjColHeader.indexOf(row)];  
                ritem = citem[row][rindex];
                        
                /* Outer variable object comes here, to access the 
                   primary and secondary objects */                        
                var path = ritem[variable].path;
                var secondary = ritem[variable].secondary;                    
                
                for (var cval in secondary){
                    /* loop through variable's secondary object keys.
                   i.e. loop through only the secondary levels or 
                   threshold keys.
                   Here we make <td> value with level and <td> 
                   with image link */         
                    var tmp = secondary[cval];
                    var colVal = tmp[0];
                    var imglink = path + '/' + tmp[1]; 
                    
                    var $img = $("<img>").attr({src: 'css/thumbnail1.png'});
                    var $link = $("<a>").attr({href: imglink,
                                               target: '_blank',
                                               'class': 'imgCls'});                    
                    $link.append($img);                               
                    
                    var trId = variable + '_' + cval.replace('.', '_');
                    
                    var $_tr = $("#" + id + " > tbody > div > table > tbody > tr[id='" + trId + "']");
                                                    
                    if (!$_tr.length){
                        /* Add the row for this level/threshold.
                          Increment the rowSpanCount, when ever
                          adding the new row <tr> for each 
                          level/threshold. */
                        var ctitle = getAbb(colVal);
                        var $tr = $("<tr>").attr({id: trId,
                                                  'class': variable + '_secondaryCls'});
                        $tr.append($("<td>").attr({'class': 'levelCls',
                                                   'title': ctitle}).append(colVal));
                        $tr.append($("<td>").attr('class','linkCls cellCls').append($link));
                        $secondaryTable.append($tr);       
                        
                    }
                    else{
                        /* Add the image link <td> alone for the 
                           rest of the columns */
                        $_tr.append($("<td>").attr('class','linkCls cellCls').append($link));
                    }                                
                                                        
                }                      
                        
            }
                    
            var $dummyDiv = $("#" + id + "  tbody  tr[id='" + variable + "_dummyTr']").children($("#" + variable + "_dummyDiv"));
            $dummyDiv.height($div.height());
                    
        }
                

            
        $("#" + id + " > tbody > tr > th > td[class='moreCls']").click(function(){
            
            if (process == 'Anomaly' || process == 'Mean'){
                selectorObjList = [modelName, process, yearIndex, year, period];
                
            }
            else if (process == 'FcstSysErr' || process == 'StatiScore'){
                selectorObjList = [modelName, process, yearIndex, year, period, subPeriodIndex, subperiod];
            }
            else{}

            var moreId = $(this).attr('id');

            var variable = moreId.split('_')[0];
            var secCls = variable + '_secondaryCls';
                                            
            var $divTable = $("#" + id + " > tbody > div[id='" + variable + "_SecondaryDiv']");
            if (!$divTable.length){
                /* Call the below fn to generate the secondary table 
                    <tr><td> elements and add to this table */
                
                if (process == 'StatiScore'){
                    except = hrRegExcept;
                }
                else{
                    except = '';
                }
                    
                genSecondaryOfTable(id, selectorObjList, variable, except);
                $(this).text('(-) Less');                    
            } 
            else{ 
                /* toggle effects */  
               var tmpObj = getPartialJsonObject(data, selectorObjList);
               
               var headersList = getSortedHeaders(tmpObj);            
                var rowHeader = headersList[0]; 
                var colHeader = headersList[1];
                var rindex = rowHeader.indexOf(variable);                 

                var $dummyDiv = $("#" + id + "  tbody  tr[id='" + variable + "_dummyTr']").children($("#" + variable + "_dummyDiv"));
                if ($divTable.is(":hidden")){                        
                    $dummyDiv.height($divTable.height());
                }                    
                $divTable.slideToggle("slow", function(){
                    if ($divTable.is(":hidden")){
                        $dummyDiv.height(0);
                    }                   
                });
                $(this).text($(this).text() === "(+) More" ? "(-) Less" : "(+) More");
                
            }
            
            var txt = $(this).text().split(' ')[1];
            var ttitle = getAbb(txt);
            $(this).attr({'title': ttitle});       
                
                            
        });          
            
        }
        
    })    
      .success(function() { $("#loading").html('Loading ...')})
      .error(function(jqXHR, textStatus, errorThrown) {
        alert('alert ' + textStatus+ jqXHR.responseText);
        for (var i in jqXHR){ alert(jqXHR[i]); }
        console.log("error " + textStatus);
        console.log("incoming Text " + jqXHR.responseText);})
      .complete(function() { $("#loading").html('Loading ...').show(3000);
                             $("#loading").html('Ready').show(8000);
                             $("#loading").hide(1000);
                              });
});
 

$(".model").live("click", function(){        
    modelName = $(this).val();
     hideOnCondition(modelName, modelName, premodelName, premodelName);
     premodelName = modelName;    
     modelid = modelName + "_Select";   
     show(modelid, 2, null);     
     processChange(modelid);

}); 


function slide_and_scroll(obj) { 
    var verticalLimit = obj.offset().top + obj.height();
    alert(verticalLimit)
    var currentVerticalScroll = $(window).scrollTop() + $(window).height(); 
    if (verticalLimit > currentVerticalScroll){ 
        var scrollTo = verticalLimit - $(window).height(); 
        $("html:not(:animated),body:not(:animated)").animate({scrollTop: scrollTo}, 500); }
    }


hideOnCondition = function(currentval, currentCls, previousval, previousCls){
    if (currentval){        
         if (currentval != previousval){
            // hide the whole class
            $('.' + previousCls + 'Cls').addClass('hideCls');      
            if ($("." + currentCls + 'Cls').hasClass('hideCls')){
                // show the selected div element
                $("." + currentCls + 'Cls').removeClass('hideCls');
            }
         }
     }
     else{        
        // selected default empty option. So hide the whole class  
        $('.' + previousCls + 'Cls').addClass('hideCls');
     }

}

show = function(id, top, showCls){
    if (showCls){
        if ($("." + showCls + 'Cls').hasClass('hideCls')){
                // show the selected div element
                $("." + showCls + 'Cls').removeClass('hideCls');
            }
    }
    //show the select box    
    $("#" + id).show();
    // show the text p element           
    $("#P" + id).show();
    // adjust the position of select box
    $("#" + id).css({"position":"absolute", "top": top + "px"});
    
}

genDivTag = function(id, attachId){
    var divtag = "<div id='div_" + id + "' class='" + id + "Cls'></div>";
    $("#" + attachId).append(divtag);
     
} 

genPTag = function(id, attachId, cls, text){
    var ptag = "<p id='P"+ id +"' class='"+ cls +"' style=''>";
    ptag += text + "</p>";
    $("#" + attachId).append(ptag);
    
}

genSelectBox = function(id, attachId, name, values, defaultText, position){
    /* position is array which contains [top, left] */
    var sbox = "<select id='" + id + "' name='" + name + "' class='selectCls' "; 
    sbox += "style='position:absolute;top:" + position[0] + "px;";
    if (position.length > 1){
        sbox +="left:" + position[1] + "px;"
    }
    sbox += "'><option value='' selected='selected'>" + defaultText + "</option>";
    for (var index in values){
        var val = values[index];
        sbox += "<option value='" + val +"'>" + val + "</option>";
    }
    sbox += "</select>";
    $('#'+attachId).append(sbox);
}

processChange = function(id){
     
    $("#" + id).change(function(){        
        process = $(this).val();
        modelProcess = modelName + '_' + process;
        processSelectId = modelProcess + '_Select';
        hideOnCondition(process, processSelectId, 
                        preprocess, modelName + '_' + preprocess + '_Select');
        preprocess = process;
        if (process){ 
            years = getValue([modelName, process], "array");     
            if (!$("#" + processSelectId).length){         
                genDivTag(processSelectId, modelName + 'Id');
                genPTag(processSelectId, 'div_' + processSelectId, 'leftTag Pyear', 'Year');
                genSelectBox(processSelectId, 'div_' + processSelectId, 'process', years, 'Select year', [40]);
            }
            // call the below function to make year change
            yearChange(processSelectId);
            // auto select if single year only available in the select box
            if (years.length == 1){                
                $("#" + processSelectId).val(years[0]).change();
            }
                              
            
        }
    });
}

yearChange = function(id){
        
    $("#" + id).change(function(){ 
        year = $(this).val();
        modelProcessYear =  modelProcess + '_' + year;
        yearSelectId = modelProcessYear + '_Select';
        hideOnCondition(year, yearSelectId, preyear, 
                        modelProcess + '_' + preyear + '_Select');
        preyear = year;        
        if (year){ 
            yearIndex = years.indexOf(year); 
            avlPeriod = getValue([modelName, process, yearIndex, year], "dictionary");
            if (!$("#" + yearSelectId).length){                               
                genDivTag(yearSelectId, 'div_' + id);
                genPTag(yearSelectId, 'div_' + yearSelectId, 'leftTag Ptime', 'Time period');
                genSelectBox(yearSelectId, 'div_' + yearSelectId, 'period', avlPeriod, 'Select period', [80]);
            }
            // call the below function to make period change 
            periodChange(yearSelectId);            
            // auto select if single time period only available in the select box
            if (avlPeriod.length == 1){                
                $("#" + yearSelectId).val(avlPeriod[0]).change();
            }
            
        }
    });
    
}

periodChange = function(id){      
        
    $("#" + id).change(function(){
        period = $(this).val();
        modelProYearPeriod = modelProcessYear + '_' + period;
        periodSelectId = modelProYearPeriod + '_Select';
        hideOnCondition(period, periodSelectId, preperiod, 
                        modelProcessYear + '_' + preperiod + '_Select');
        preperiod = period;
        if (period){
            var periodTableId = modelProYearPeriod + '_Table';
            if (!$("#div_" + periodSelectId).length){
                    genDivTag(periodSelectId, 'div_' + id);  
               }
               
            if (process == 'Anomaly' || process == 'Mean'){
                selectorObjList = [modelName, process, yearIndex, year, period];
                if (!$("#" + periodTableId).length){
                    genTable(periodTableId, "#div_" + periodSelectId, selectorObjList);               
                }
                else{
                    $("#" + periodTableId).show();                    
                }
            }
            else if (process == 'FcstSysErr' || process == 'StatiScore'){
            
                avlSubPeriod = getValue([modelName, process, yearIndex, year, period], "array");
                if (!$("#" + periodSelectId).length){                               
                    genDivTag(periodSelectId, 'div_' + id);
                    //genPTag(periodSelectId, 'div_' + periodSelectId, 'leftTag', 'Time period');
                    genSelectBox(periodSelectId, 'div_' + periodSelectId, 'subperiod', avlSubPeriod, 'Select ' + period, [80, 130]);
                }
                // call the below function to make sub period change 
                subPeriodChange(periodSelectId);            
                // auto select if single time sub period only available in the select box
                if (avlSubPeriod.length == 1){                
                    $("#" + periodSelectId).val(avlSubPeriod[0]).change();
                }
                           
            }

            else{
                alert("add process function for " + process);
            }
        }    
    });
}


subPeriodChange = function(id){
    $("#" + id).change(function(){
        subperiod = $(this).val();
        modelProYearPPeriod = modelProYearPeriod + '_' + subperiod;
        subPeriodSelectId = modelProYearPPeriod + '_Select';
        hideOnCondition(period, subPeriodSelectId, presubperiod, 
                        modelProYearPeriod + '_' + presubperiod + '_Select');
        presubperiod = subperiod;
        if (subperiod){
            subPeriodIndex = avlSubPeriod.indexOf(subperiod); 
            var selectorObjList = [modelName, process, yearIndex, year, period, subPeriodIndex, subperiod];
            if (process == 'FcstSysErr'){
                var subPeriodTableId = modelProYearPPeriod + '_Table';
                if (!$("#" + subPeriodTableId).length){ 
                    genDivTag(subPeriodSelectId, 'div_' + id); 
                    genTable(subPeriodTableId, "#div_" + subPeriodSelectId, selectorObjList);
                }
                else{
                    $("#" + subPeriodTableId).show();                
                }
            }
            else if (process == 'StatiScore'){

                if (!$("#" + subPeriodSelectId).length){
                    avlHourRegion = getValue(selectorObjList, "array");
                    if ($.inArray('Region', avlHourRegion) > -1 && avlHourRegion.length > 1){
                        // 'Region' is exists in the array 
                        genDivTag(subPeriodSelectId, 'div_' + id);                         
                        genPTag(subPeriodSelectId, 'div_' + subPeriodSelectId, 
                                'leftTag Phrreg', 'Forecast Hour/Region');
                        genSelectBox(subPeriodSelectId, 'div_' + subPeriodSelectId, 
                                     'period', ['By Hour', 'By Region'], 
                                     'Select Hour/Region', [120]);                        
                    }
                    else{
                        // only Hours exists.
                    }            
               }
               hourRegionChange(subPeriodSelectId);
                
                
            } 
            else{
             //
            } 
        }
    });
}

hourRegionChange = function(id){
    $("#" + id).change(function(){
        hrReg = $(this).val().split(' ')[1];        
        var hrRegSelectId = modelProYearPeriod + '_' + hrReg + '_Select';
        hideOnCondition(hrReg, hrRegSelectId, prehrReg, 
                        modelProYearPeriod + '_' + prehrReg + '_Select');
        prehrReg = hrReg;
        if (hrReg){             
            var selectorObjList = [modelName, process, yearIndex, year, period, subPeriodIndex, subperiod];
            if (hrReg == 'Hour') hrRegExcept = ['Region'];
            if (hrReg == 'Region') {
                /* Make array copy */
                hrRegExcept = avlHourRegion.slice();
                hrRegExcept.pop('Region');
            }
            
            var hrRegTableId = modelProYearPeriod + '_' + hrReg + '_Table';
            if (!$("#div_" + hrRegSelectId).length){
                genDivTag(hrRegSelectId, 'div_' + id);
                genTable(hrRegTableId, "#div_" + hrRegSelectId, selectorObjList, hrRegExcept);
            }
            else{
                $("#" + hrRegTableId).show();                
            }
        
        }
        
    });
}


$(".imgCls").live("mouseover", function(){                            
    imglink = $(this).attr('href');
    imgpre = '<img src ="' + imglink + '", width = "540", height = "480"/>'
    preview = '<p><b>Preview</b></p>'                           
    $("#preview").html(preview + imgpre);
});

$(".imgCls").live("mouseout", function(){                                                        
    $("#preview").html('<img src="css/dummy.png" width="180", height="180"/>');
});
                              



