$(function(){

    //JSONオブジェクトを文字列に変える
    function getJsonStr(json){
        return JSON.stringify(json);
    }

    //CSRF Tokenを取得する
    function getCSRFToken(){
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        return csrftoken;
    }

    //年度期から問題を取得する
    function ajax_getquestionpm(child_class, query ){
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/exam/ajax_getquestionpm/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {

            $( child_class ).children().remove();
            $( '#questionans').children().remove();

            $.each( data['q_list'], function(index,value){

                console.log( value['qfn'] );
                console.log( value['afn'] );
                $tr = $( '<tr>' );
                $td = $('<td>').append( $('<a href=/static/exam/pdf/question_pm/' + value['qfn'] + '>').text( value['qfn']).attr('target','_blank') );
                $tr.append( $td );
                if( value['afn'] != 'ファイルなし' ){
                    $td = $( '<td>' ).append( $('<a href=/static/exam/pdf/question_pm/' + value['afn'] + '>').text( value['afn']).attr('target','_blank') );
                }else{
                    $td = $( '<td>' ).text( value['afn'] );
                }


                $tr.append( $td );
                $(child_class).append( $tr );
            });

        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });
    }

    //subjectからtitleを取得する
    function ajax_gettitle(child_class, query ){
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/exam/ajax_gettitle/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $( child_class ).children().remove();
            for( var i = 0 , len=data.length; i<len;++i){
                $( child_class).append(  $('<option>').attr('value',data[i]['q_num']).text( data[i]['q_title'] + '(' + data[i]['q_num'] + ')') );
            }

        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });
    }
    //subjectからtitleを取得する
    function ajax_getquestionjs(child_class, query ){
        console.log( query );
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/exam/ajax_getquestionjs/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $( child_class ).children().remove();
            console.log( data );
            for( var i = 0 , len=data.length; i<len;++i){
                console.log( data[i]['filename']);
                $tr = $("<tr>");
                $a = $("<a>").attr('href','/static/exam/pdf/question_js/' + data[i]['filename']).attr('target','_blank').text(data[i]['filename']);
                $td = $("<td>").append( $a );
                $tr.append( $td );
                $td = $("<td>").text( data[i]['q_content']);
                $tr.append( $td );
                $( child_class).append( $tr );
            }

        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });
    }
    $("#subject").on('change',function(){
        //ユーザのidを送信する
        var json = {'subject' : $('#subject').val() };
        //alert( json );
        ajax_gettitle( '#title' , json );
    });

    $("#title").on('change',function(){
        //alert("title change");
        var json = {'subject':$("#subject").val() , 'title':$("#title").val()};
        ajax_getquestionjs('#questionjs' , json );
    });
});