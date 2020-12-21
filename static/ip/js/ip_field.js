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


    //大分類を変更
    $("#ip_l_field").on('change',function(){
        //alert("ip_l_field");
        //ユーザのidを送信する
        var json = {'ip_l_field' : $('#ip_l_field').val() };
        //alert( json );
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/ip/ajax_ip_l_field_change/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( json ),

        }).done( (data) => {
            $('#ip_m_field').children().remove();
            $('#ip_m_field').append( $('<option>') );
            $('#ip_s_field').children().remove();
            $('#question').children().remove();

            for( var i = 0 ;i < data['field_list'].length ; i++){
                $option = $("<option>").val(data['field_list'][i]['ip_m_field']).text(data['field_list'][i]['ip_m_field']);
                $('#ip_m_field').append( $option );
            }

            for( var i = 0 ; i < data['question_list'].length ; i++ ){
                $img = $('<img>').attr('src','/static/ip/question/' + data['question_list'][i]['ip_id'] + ".png");
                $p = $('<p>').append( $('<spam>').text('【' + data['question_list'][i]['ip_period'] + '】'))
                        .append( $('<spam>').text(' 大分類:' + data['question_list'][i]['ip_l_field']))
                        .append( $('<spam>').text(' 中分類:' + data['question_list'][i]['ip_m_field']))
                        .append( $('<spam>').text(' 小分類:' + data['question_list'][i]['ip_s_field']));

                $div = $('<div>').append( $p ).append( $img ).attr('style','margin-bottom:40px;');
                $pa = $('<p>').text( "答え：【" + data['question_list'][i]['ip_answer'] + "】");
                $div.append( $pa );
                $('#question').append( $div );
            }

        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });

    });

    //中分類を変更
    $("#ip_m_field").on('change',function(){
        //alert("ip_l_field");
        //ユーザのidを送信する
        var json = {'ip_l_field' : $('#ip_l_field').val() , 'ip_m_field': $('#ip_m_field').val() };
        //alert( json );
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/ip/ajax_ip_m_field_change/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( json ),

        }).done( (data) => {
            $('#ip_s_field').children().remove();
            $('#ip_s_field').append( $('<option>') );
            $('#question').children().remove();

            for( var i = 0 ;i < data['field_list'].length ; i++){
                $option = $("<option>").val(data['field_list'][i]['ip_s_field']).text(data['field_list'][i]['ip_s_field']);
                $('#ip_s_field').append( $option );
            }

            for( var i = 0 ; i < data['question_list'].length ; i++ ){
                $img = $('<img>').attr('src','/static/ip/question/' + data['question_list'][i]['ip_id'] + ".png");
                $p = $('<p>').append( $('<spam>').text('【' + data['question_list'][i]['ip_period'] + '】'))
                        .append( $('<spam>').text(' 大分類:' + data['question_list'][i]['ip_l_field']))
                        .append( $('<spam>').text(' 中分類:' + data['question_list'][i]['ip_m_field']))
                        .append( $('<spam>').text(' 小分類:' + data['question_list'][i]['ip_s_field']));

                $div = $('<div>').append( $p ).append( $img ).attr('style','margin-bottom:40px;');
                $pa = $('<p>').text( "答え：【" + data['question_list'][i]['ip_answer'] + "】" );
                $div.append( $pa );
                $('#question').append( $div );
            }

        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });

    });

    //小分類を変更
    $("#ip_s_field").on('change',function(){
        //alert("ip_s_field");
        //ユーザのidを送信する
        var json = {'ip_s_field':$('#ip_s_field').val() };
        //alert( json );

        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/ip/ajax_ip_s_field_change/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( json ),

        }).done( (data) => {

            $('#question').children().remove();

            for( var i = 0 ; i < data['question_list'].length ; i++ ){
                $img = $('<img>').attr('src','/static/ip/question/' + data['question_list'][i]['ip_id'] + ".png");
                $p = $('<p>').append( $('<spam>').text('【' + data['question_list'][i]['ip_period'] + '】'))
                        .append( $('<spam>').text(' 大分類:' + data['question_list'][i]['ip_l_field']))
                        .append( $('<spam>').text(' 中分類:' + data['question_list'][i]['ip_m_field']))
                        .append( $('<spam>').text(' 小分類:' + data['question_list'][i]['ip_s_field']));

                $div = $('<div>').append( $p ).append( $img ).attr('style','margin-bottom:40px;');
                $pa = $('<p>').text( "答え：【" + data['question_list'][i]['ip_answer'] + "】" );
                $div.append( $pa );
                $('#question').append( $div );
            }

        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });

    });

});