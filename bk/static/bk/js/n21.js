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
    $("#formControlRange").val( 800 / 1400 * 100 );
    //スライダーのイベント
    $("#formControlRange").on('change',function(){
        
        var q_size = ($(this).val() * 1400 / 100) ;
        $(".q_img").attr("style","width:" + q_size + "px;" );
        $("#txtSize").val( q_size );
    });
    //サイズのイベント
    $("#txtSize").on('change',function(){
        var q_size = $(this).val();
        $(".q_img").attr("style","width:" + q_size + "px;" );
        $("#formControlRange").val( q_size / 1400 * 100);

    });

    $("#s_test").on('change',function(){

        query = {'b_field':$(this).val() };

        $("#t_id").text( "テストID:" + query['b_field'] );

        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/bk/ajax_n21_getquestion/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#qtable').children().remove();
            $('#qanswer').children().remove();

            for( var i = 0 ;  i < data.qlist.length ; i++){

                $td1 = $('<td>').text("第" + data.qlist[i]['b_times'] + "回 問" + data.qlist[i]['b_que1'] + " (" + data.qlist[i]['b_que2'] + ")");
                $td1.attr("style","font-size:14pt;");
                $tr1 = $("<tr>").append( $td1 );

                $img = $("<img src='/static/bk/question/" + data.qlist[i]['b_id'] + ".png'>");
                $img.attr("style","width:800px;");
                $img.attr("class","q_img");
                $td2 = $('<td>').append($img);
                $tr2 = $('<tr>').append($td2);

                $('#qtable').append( $tr1 );
                $('#qtable').append( $tr2 );

                $atr = $("<tr colspan='4'>").append( $td1 ).attr("style","border:1px solid black");
                $('#qanswer').append( $atr );
                $btr = $("<tr>")
            }

        }).fail( (data)=>{
            alert('fail');
        }).always( (data) => {

        });

    });

    //解答用紙印刷画面へ
    $('#btnKaitou').on('click',function(){
        t_id = $('#s_test').val();
        console.log( t_id );
        window.location.href = "/jg/answersheetprint/?t_id=" + t_id;
    });

});