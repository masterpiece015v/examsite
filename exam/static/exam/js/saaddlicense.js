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
    $("#btn_per").on('click',function(){
        query = {'id':$("#id").val()};
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/exam/saaddlicense_conf/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $("#id").children().remove();
            
            for( var i = 0 ; i < data.length ;  i = i + 1 ){
                $op = $("<option>")
                $op.val( data[i]['id'] )
                $op.text( data[i]['l_num'] +"," + data[i]['adr_date'] + "," + (data[i]['check'] ? '許可済' : '未許可')  )
                $("#id").append( $op )
            }

            $('#modal-progress').modal('hide');

        }).fail( (data)=>{
            alert('fail');
        }).always( (data) => {

        });


    });
    $("#org").on('change',function(){
        query = {'o_id':$(this).val()};
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/exam/saaddlicense_filter/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $("#id").children().remove();
            
            for( var i = 0 ; i < data.length ;  i = i + 1 ){
                $op = $("<option>")
                $op.val( data[i]['id'] )
                $op.text( data[i]['l_num'] +"," + data[i]['adr_date'] + "," + (data[i]['check'] ? '許可済' : '未許可')  )
                $("#id").append( $op )
            }


            $('#modal-progress').modal('hide');

        }).fail( (data)=>{
            alert('fail');
        }).always( (data) => {

        });

    });

});