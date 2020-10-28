$(function(){
    //4桁のコードを作る
    function getcode4( code ){
        if(code < 10){
            return '000' + String(code);
        }else if(code < 100){
            return '00' + String(code);
        }else if(code < 1000){
            return '0' + String(code);
        }else{
            return String(code);
        }
    }

    //排他的でランダムな値を取得する
    function* getrandom( max ){
        
        var ary = new Array( max );

        for(var i = 0 ; i < max ; i++ ){
                   
            var r = Math.floor( Math.random() * max + 1);
        
            while( ary[r] == 1 ){
                r = Math.floor( Math.random() * max + 1);
            }
            ary[r] = 1;
            yield r;
        }
    }

    //JSONオブジェクトを文字列に変える
    function getJsonStr(json){
        return JSON.stringify(json);
    }

    //CSRF Tokenを取得する
    function getCSRFToken(){
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        return csrftoken;
    }

    //問題番号を取得するajax
    function ajax_gettid(child_class, query ){
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/jg/ajax_gettid/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            //$('#question').children().remove();
            $( child_class ).children().remove();
            for( var i = 0 , len=data['t_id'].length; i<len;++i){
                //全クリア

                //追加
                //Object.keys(data).forEach( function( key ){
                $option = $('<option>').val( data['t_id'][i] ).text( data['t_id'][i] );
                //alert( data['t_id'][i] );
                $( child_class ).append( $option );
                //});
             }

        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });
    }
    //問題を取得するajax
    function ajax_getresult(child_class, query ){
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/jg/ajax_getresult/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#score').text(data['score']);
            $('#total').text(data['total']);

            $('#resultdata').children().remove();
            for( var i = 0 , len=data['t_num'].length; i<len;++i){
                code4 = getcode4(i+1);
                $tr = $("<tr id='tr" + code4 + "'>");
                //Object.keys(data[i]).forEach( function( key ){
                //    $td = $('<td>').text( data[i][key] );
                //    $tr.append( $td );
                //});
                $td = $('<td>').text( data['t_num'][i]);
                $tr.append( $td );
                $td = $("<td>").text( data['q_id'][i]);
                $tr.append( $td );
                $td = $('<td>').text( data['r_answer'][i]);
                $tr.append( $td );
                $td = $('<td>').text( data['q_answer'][i]);
                $tr.append( $td );
                $td = $('<td>').text( data['mb'][i]);
                if( data['mb'][i]=='0'){
                    $tr.attr('style','background-color:red;color:white;');
                }
                $tr.append( $td );
                $img = $("<img src='/static/jg/image/question/" + data['q_id'][i] + ".png' alt='" + data['q_id'][i] + "' style='width:400px'>" );
                $tr.append( $('<td>').append( $img ) );


                $('#resultdata').append( $tr );
             }

        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });
    }

    //ユーザのリストをクリック
    $("#lst_user").on('click',function(){
        //ユーザのidを送信する
        var json = {'u_id' : $('#lst_user').val() }
        ajax_gettid( '#lst_tid' , json );
    });

    //テストのリストをクリック
    $('#lst_tid').on('click',function(){
        var json = {'u_id' : $('#lst_user').val() , 't_id':$('#lst_tid').val()};
        ajax_getresult( '#resultdata' , json );
    });
});