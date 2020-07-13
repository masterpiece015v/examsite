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

    //ユーザ名からテストIDを取得する
    function ajax_get_test_id_list(child_class, query ){
        console.log( getJsonStr(query) );
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/exam/ajax_gettestidlist/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#lst_test').children().remove();
            $('#lst_test').append( $('<option>').val('all').text('all'));
            for( var i = 0 ; i < data.length ; i++){
                $option = $('<option>').val( data[i]['t_id'] ).text(data[i]['t_id'] );
                $('#lst_test').append( $option );
            }
        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });
    }

    //テストIDをクリック
    function ajax_get_test_id_result(child_class, query ){
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/exam/ajax_gettestidresult/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#resultdata').children().remove();
            for( var i = 0 ; i < data.length ; i++){
                $tr = $('<tr>')
                $td1 = $('<td>').text(data[i]['u_id'])
                $td2 = $('<td>').text(data[i]['u_name'])
                $td3 = $('<td>').text(data[i]['positive'])
                $tr.append( $td1 );
                $tr.append( $td2 );
                $tr.append( $td3 );
                $('#resultdata').append( $tr );
            }
        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });
    }
    //ユーザ名をクリックしたときのイベント
    $('#lst_make_test').on('click',function(){
        var json = {'u_id':$('#lst_make_test').val()};
        ajax_get_test_id_list('lst_test',json);
    });
    //ユーザ名をクリックしたときのイベント
    $('#lst_test').on('click',function(){
        var json = {'t_id':$('#lst_test').val()};
        ajax_get_test_id_result('resultdata',json);
    });
});
