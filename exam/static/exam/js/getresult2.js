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

    //問題を取得するajax
    function ajax_getresult2(child_class, query ){
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/exam/get_result_bunya/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {

            $('#resultdata').children().remove();

            $('#l_list').children().remove();

            for( key in data['l_dics']){
                $option = $('<option>').val( key ).text(data['l_dics'][key]);
                $('#l_list').append( $option );
            }
            /*
            for( var i = 0 , len=data['q_id'].length; i<len;++i){
                $tr = $("<tr>");
                //Object.keys(data[i]).forEach( function( key ){
                //    $td = $('<td>').text( data[i][key] );
                //    $tr.append( $td );
                //});
                $td = $('<td>').text( data['q_id'][i]);
                $tr.append( $td );
                $td = $('<td>').text( data['l_name'][i]);
                $tr.append( $td );
                $td = $('<td>').text( data['m_name'][i]);
                $tr.append( $td );
                $td = $('<td>').text( data['s_name'][i])
                $tr.append( $td );

                $('#resultdata').append( $tr );
             }
             */
        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });
    }

    //ユーザのリストをクリック
    $("#lst_user").on('click',function(){
        //ユーザのidを送信する
        var json = {'u_id' : $('#lst_user').val() };
        ajax_getresult2( '#lst_tid' , json );
    });

    //分類を変更したときのコールバック関数
    function ajax_get_list(child_class, query){
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/exam/get_" + child_class + "/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $( "#" + child_class ).children().remove();

            Object.keys(data).forEach( function( key ){
                $option = $('<option>').val(key).text(data[key]);
                $('#' + child_class).append( $option );
            });
        }).fail( (data)=>{
            alert( 'Error' );
        }).always( (data) => {
        });
    }
    //大分類をクリック
    $("#l_list").on('change',function(){
        //alert("l_list_change");
        var json = {'u_id':$('#lst_user').val(),'l_id' : $('#l_list').val() };
        //alert("l_list_change");
        ajax_get_list( '#m_list',json );
    });
    //中分類をクリック
    $('#m_list').on('change',function(){
        var json = { 'u_id' : $('#lst_user').val() , 'l_id':$('#l_list').val() ,'m_list':$('#m_list').val()};
        ajax_get_list('#s_list',json);
    });

});
