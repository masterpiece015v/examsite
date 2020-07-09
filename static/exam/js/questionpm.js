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

            for( var i = 0 , len=data.length; i<len;++i){
                $p = $( '<p>' ).append( $('<a href=/static/exam/pdf/question_pm/' + data[i]['q_id'] + '.png alt=' + data[i]['q_id'] + '>').attr('class','question') );
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
    //
    $("#classify").on('change',function(){
        //ユーザのidを送信する
        var json = {'classify' : $('#classify').val() }
        ajax_getquestionpm( '#questionpm' , json );
    });

});