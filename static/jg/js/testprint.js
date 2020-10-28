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

        query = {'t_id':$(this).val() };

        $("#t_id").text( "テストID:" + query['t_id'] );

        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/jg/ajax_gettestprint/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#qtable').children().remove();
            $('#qanswer').children().remove();

            for( var i = 0 ;  i < data.length ; i++){

                $td1 = $('<td>').text(data[i]['t_num'] + ",【試験番号】" + data[i]['q_id'] + ",【中分類】" + data[i]['m_name'] + ",【小分類】" + data[i]['s_name']);
                $td1.attr("style","font-size:14pt;");
                $tr1 = $("<tr>").append( $td1 );

                $img = $("<img src='/static/jg/image/question/" + data[i]['q_id'] + ".png'>" );
                $img.attr("style","width:800px;");
                $img.attr("class","q_img");
                $td2 = $('<td>').append($img);
                $tr2 = $('<tr>').append($td2);

                $('#qtable').append( $tr1 );
                $('#qtable').append( $tr2 );

            }

            for( var i = 0 ; i < 20 ; i++ ){
                //alert( data.length );
                if( data.length <= 20 ){
                    //console.log( data[i]['t_num']);
                    if( i < data.length) {
                        $tr3 = $('<tr>').append(
                            $("<td>").text( data[i]['t_num']),
                            $("<td>").text( data[i]['q_answer'])
                        );
                    }
                } else if( data.length <= 40 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i]['t_num']) ,$("<td>").text(data[i]['q_answer']) );
                    if( (i + 20 ) < data.length ) {
                        $tr3.append( $("<td>").text(data[i+20]['t_num']) , $("<td>").text(data[i+20]['q_answer']));
                    }
                } else if( data.length <= 60 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i]['t_num']) , $("<td>").text(data[i]['q_answer']) );
                    $tr3.append( $("<td>").text(data[i+20]['t_num']) , $("<td>").text(data[i+20]['q_answer']) );
                    if((i+40) < data.length ){
                        $tr3.append( $("<td>").text(data[i+40]['t_num']) , $("<td>").text(data[i+40]['q_answer']) );
                    }
                } else if ( data.length <= 80 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i]['t_num']) , $("<td>").text(data[i]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+20]['t_num']) , $("<td>").text(data[i+20]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+40]['t_num']) , $("<td>").text(data[i+40]['q_answer']));

                    if((i+60) < data.length ){
                        $tr3.append( $("<td>").text(data[i+60]['t_num']) , $("<td>").text(data[i+60]['q_answer']));
                    }
                }

                $('#qanswer').append($tr3);
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