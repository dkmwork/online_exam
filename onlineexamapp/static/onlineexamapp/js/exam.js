jQuery(function(){
    jQuery('.datepicker').datepicker();

    // select the year from exam date and add to the year field.

    jQuery('#id_exam_date').change(function(){
        var jsDate=jQuery('#id_exam_date').datepicker('getDate');
        var jsyear=jsDate.getFullYear();
        jQuery('#id_exam_year').val(jsyear)
        jQuery('#id_exam_year').prop('readonly',true)
    })
    function createpaginationcontrols(count,linktobeattached){
        jQuery('#'+linktobeattached).empty()
        for(var i=0;i<count/2;i++){
            var anchortag=document.createElement('a')
            anchortag.className="pagination"
            anchortag.textContent=i+1
            anchortag.value=i+1
            anchortag.style.display="inline-block"
            jQuery('#'+linktobeattached).append(anchortag)
        }
    }
    jQuery('#id_question_type').change(function(){
        //alert(jQuery(this).val())
        if(jQuery(this).val()!="Multiple_choice"){
           jQuery('#id_max_no_option').prop('readonly',true) 
        }
        else{
            alert(jQuery(this).val())
            jQuery('#id_max_no_option').prop('readonly',false)
        }
    })


    jQuery ('#exampage_links').on('click','a',function(event){
        var examname=jQuery('#partyinfo').val()
        var examdate=jQuery('#gameinfo').val()
        pagenum=jQuery(this).val()
        jQuery.ajax({
            type:"GET",
            url:"examsearchinfo",
            data:{
                examname:examname,
                examdate:examdate,
                page:pagenum,
            },
            success:function(response){
                jQuery('#examlist_runtime tbody').empty()
                jQuery.each(response,function(i,item){
                    if(i!='total_count'){
                        var pexamid=item.examid
                        var pexam=item.examname
                        var pcode=item.examcode
                        var pduration=item.examduration
                        var pquestion=item.examquestion
                        var ptime=item.examtime
                        var pdate=item.examdate
                        var markup=`<tr><td>${pexam}</td><td>${pcode}</td><td>${pduration}</td><td>${pquestion}</td><td>${ptime}</td><td>${pdate}</td><td><a data-examid=${pexamid} class="btn btn-danger">Edit</a></td></tr>`
                        jQuery("#examlist_runtime tbody").append(markup)
                    }
                    else{counter=item.queryset_count}
                })
            }
        })
        event.preventDefault()
        return false
    })

    jQuery('#examget').click(function(){
        var searchname=jQuery('#examinfo').val()
        var searchdate=jQuery('#dateinfo').val()
        jQuery.ajax({
            type:"GET",
            url:"examsearchinfo",
            data:{
                examname:searchname,
                examdate:searchdate,
            },
        success:function(response){
            //console.log(response)
            jQuery('#examlist_runtime tbody').empty()
            var counter=0
            jQuery.each(response,function(i,item){
                if(i!='total_count'){
                    //console.log(item)
                    var pexamid=item.examid
                    var pexam=item.examname
                    var pcode=item.examcode
                    var pcat=item.examcat
                    var pduration=item.examduration
                    var pquestion=item.examquestion
                    var pmark=item.exammark
                    var plevel=item.examlevel
                    var ptime=item.examtime
                    var pdate=item.examdate
                    var pyear=item.examyear
                    var ptype=item.examtype
                    //var link=document.createElement('a')
                    //link.attr('href',"'examedit' examid=item.exam_id")
                    //link.text("Edit");
                    //link.addClass("link");
                    //jQuery('#edit_links').append(link)
                    //var markup="<tr><td>"+pexam+"</td><td>"+pcode+"/<td><td>"+pcat+"</td><td>"+pduration+"</td><td>"+pquestion+"</td><td>"+pmark+"</td><td>"
                    //+plevel+"</td><td>"+ptime+"</td><td>"+pdate+"</td><td>"+pyear+"</td><td>"+ptype+"</td></tr>"
                    // var markup="<tr><td>"+pexam+"</td><td>"+pcode+"</td><td>"+pduration+"</td><td>"+pquestion+"</td><td>"
                    // +ptime+"</td><td>"+pdate+"</td><td>"+html(link)+"</td></tr>"                                       // "{% url 'examedit' examid=item.exam_id %}"
                    var markup=`<tr><td>${pexam}</td><td>${pcode}</td><td>${pduration}</td><td>${pquestion}</td><td>${ptime}</td><td>${pdate}</td><td>
                    <a data-examid=${pexamid} href=?examid=${pexamid} class="btn btn-danger">Edit</a></td></tr>`
                    jQuery("#examlist_runtime tbody").append(markup)
                }

                else{counter=item.queryset_count}
            })
            createpaginationcontrols(counter,"exampage_links")
        }   
        })
    })

    //href="?{% if partyname %}partyname={{partyname}}&{%endif%}{% if categoryname %}categoryname={{categoryname}}&{%endif%}{% if menuname %}menuname={{menuname}}&{%endif%}{% if menutype %}menutype={{menutype}}&{%endif%}{% if menuarea %}menuarea={{menuarea}}&{%endif%}page=1">&laquo; first</a>

    jQuery("#examlist_runtime tbody").on('click','a',function(event){
        //alert("hi")
       var anchor_tag=event.currentTarget
       var examid=anchor_tag.getAttribute('data-examid')
       alert(examid)
        event.preventDefault()
        //var examname=jQuery('#exam_detailsid').val()
        //console.log(examname)
        jQuery.ajax({
            type:"GET",
            url:"examsearchpagination",
            data:{
                examid:examid
            },
            success:function(response){
                //alert('hi')
                console.log(response)
                
                    var ename=response.exam_name
                    var ecode=response.exam_code
                    var ecat=response.exam_is_cat
                    var eduration=response.exam_duration
                    var equestion=response.exam_no_questions
                    var emark=response.exam_cut_of_mark
                    var elevel=response.exam_level
                    var etime=response.exam_time
                    var edate=response.exam_date
                    var eyear=response.exam_year
                    var etype=response.exam_type
                    var markup="<tr><td>"+ename+"</td><td>"+ecode+"</td><td>"+ecat+"</td><td>"+eduration+"</td><td>"+equestion+"</td><td>"+emark+
                    "</td><td>"+elevel+"</td><td>"+etime+"</td><td>"+edate+"</td><td>"+eyear+"</td><td>"+etype+"</td></tr>"
                    //console.log(markup)
                    jQuery('#examinfo tbody').append(markup)
                
            }
        })
    })


})

