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
    function ajax_getquestion_period(child_class, query ){
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/exam/ajax_getquestion_period/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $( child_class ).children().remove();
            for( var i = 0 , len=data.length; i<len;++i){
                $p = $( '<p>' ).append( $('<img src=/static/exam/image/question/' + data[i]['q_id'] + '.png alt=' + data[i]['q_id'] + '>').attr('class','question') );
                $( child_class ).append( $p );
                $p = $('<p>');
                $p.append( $('<span>').text('答え:') );
                $p.append( $('<span>').attr('class','answer').text( data[i]['q_answer']));
                $( child_class).append( $p );
                //console.log( '/static/exam/image/question/' + data[i] + '.png' );
            }

        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });
    }
    //中分類コードから問題を取得する
    function ajax_getquestion_classify(child_class, query ){
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/exam/ajax_getquestion_classify/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $( child_class ).children().remove();
            for( var i = 0 , len=data.length; i<len;++i){
                $p = $( '<p>' ).append( $('<img src=/static/exam/image/question/' + data[i]['q_id'] + '.png alt=' + data[i]['q_id'] + '>') );
                $( child_class ).append( $p );
                $p = $('<p>');
                $p.append( $('<span>').text('答え:') );
                $p.append( $('<span>').attr('class','answer').text( data[i]['q_answer']));
                $( child_class).append( $p );
                console.log( '/static/exam/image/question/' + data[i]['q_id'] + '.png' );
            }

        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });
    }

    function ajax_getperiod(child_class,json){
        $.ajaxSetup({
            beforeSend : function(xhr,settings){
                xhr.setRequestHeader( 'X-CSRFToken',getCSRFToken());
            }
        });
        $.ajax({
            type:"POST",
            url:"/exam/mainpage_ajax_getperiod/",
            dataType:'json',
            contentType:'charset=utf-8',
            data:getJsonStr( json ),
        }).done( (data) => {
            $(child_class).children().remove();
            for( i = 0 ; i < data.length ; i++){
                $op = $('<option>').val(data[i]['period']).text(data[i]['name']);
                $(child_class).append( $op );
            }
        }).fail((data)=>{

        }).always((data)=>{

        });
    }

    //テストをクリック
    $('#test').on('click',function(){
        var json = {'q_test':$('#test').val() };
        ajax_getperiod('#period',json);
    });

    //年度期をクリック
    $("#period").on('click',function(){
        //ユーザのidを送信する
        var json = {'q_period' : $('#period').val() ,'q_test':$('#test').val() };
        console.log( json );
        ajax_getquestion_period( '#question' , json );
    });

    //中分類をクリック
    $('#classify').on('click',function(){
        var json = {'m_id' : $('#classify').val(),'q_test':$('#test').val() };
        ajax_getquestion_classify( '#question' , json );
    });
});