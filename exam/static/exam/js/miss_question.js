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


    $("#users").on('change',function(){

        query = {'u_id':$(this).val(),'m_u_id':$('#makeusers').val() };

        console.log( query );

        //$("#u_id").text( "テストID:" + query['t_id'] );

        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/exam/ajax_miss_question/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#qtable').children().remove();
            $('#qanswer1').children().remove();
            $('#qanswer2').children().remove();
            $('#qanswer3').children().remove();

            for( var i = 0 ;  i < data.length ; i++){

                $td1 = $('<td>').text("【試験番号】" + data[i]['q_id'] + ",【中分類】" + data[i]['m_name'] + ",【小分類】" + data[i]['s_name']);
                $td1.attr("style","font-size:12pt;");
                $tr1 = $("<tr>").append( $td1 );

                $img = $("<img src='/static/exam/image/question/" + data[i]['q_id'] + ".png'>" );
                $img.attr("style","width:800px;");
                $img.attr("class","q_img");
                $td2 = $('<td>').append($img);
                $tr2 = $('<tr>').append($td2);

                $('#qtable').append( $tr1 );
                $('#qtable').append( $tr2 );

            }

            console.log( data.length );

            for( var i = 0 ; i < 25 ; i++ ){
                if( data.length <= 25 ){
                    $tr3 = $('<tr>');
                    $tr3.append( $("<td>").text( data[i]['q_id']),$("<td>").text(data[i]['q_answer']));
                } else if( data.length <= 50 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text( data[i]['q_id']),$("<td>").text(data[i]['q_answer']) );
                    if( (i+25) < data.length ) {
                        $tr3.append( $("<td>").text(data[i+25]['q_id']) , $("<td>").text(data[i+25]['q_answer']));
                    }
                } else if( data.length <= 75 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i]['q_id']) , $("<td>").text(data[i]['q_answer']) );
                    $tr3.append( $("<td>").text(data[i+25]['q_id']) , $("<td>").text(data[i+25]['q_answer']) );
                    if((i+50) < data.length ){
                        $tr3.append( $("<td>").text(data[i+50]['q_id']) , $("<td>").text(data[i+50]['q_answer']) );
                    }
                } else if ( data.length <= 100 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i]['q_id']) , $("<td>").text(data[i]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+25]['q_id']) , $("<td>").text(data[i+25]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+50]['q_id']) , $("<td>").text(data[i+50]['q_answer']));

                    if((i+75) < data.length ){
                        $tr3.append( $("<td>").text(data[i+75]['q_id']) , $("<td>").text(data[i+75]['q_answer']));
                    }
                } else if ( data.length <= 125 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i]['q_id']) , $("<td>").text(data[i]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+25]['q_id']) , $("<td>").text(data[i+25]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+50]['q_id']) , $("<td>").text(data[i+50]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+75]['q_id']) , $("<td>").text(data[i+75]['q_answer']));
                    if((i+100) < data.length ){
                        $tr3.append( $("<td>").text(data[i+100]['q_id']) , $("<td>").text(data[i+100]['q_answer']));
                    }
                } else if ( data.length <= 150 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i]['q_id']) , $("<td>").text(data[i]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+25]['q_id']) , $("<td>").text(data[i+25]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+50]['q_id']) , $("<td>").text(data[i+50]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+75]['q_id']) , $("<td>").text(data[i+75]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+100]['q_id']) , $("<td>").text(data[i+100]['q_answer']));
                    if((i+125) < data.length ){
                        $tr3.append( $("<td>").text(data[i+125]['q_id']) , $("<td>").text(data[i+125]['q_answer']));
                    }
                } else if ( data.length <= 175 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i]['q_id']) , $("<td>").text(data[i]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+25]['q_id']) , $("<td>").text(data[i+25]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+50]['q_id']) , $("<td>").text(data[i+50]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+75]['q_id']) , $("<td>").text(data[i+75]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+100]['q_id']) , $("<td>").text(data[i+100]['q_answer']));
                    if((i+125) < data.length ){
                        $tr3.append( $("<td>").text(data[i+125]['q_id']) , $("<td>").text(data[i+125]['q_answer']));
                    }
                    $('#qanswer1').append($tr3);
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i+150]['q_id']) , $("<td>").text(data[i+150]['q_answer']));
                } else if ( data.length <= 200 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i]['q_id']) , $("<td>").text(data[i]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+25]['q_id']) , $("<td>").text(data[i+25]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+50]['q_id']) , $("<td>").text(data[i+50]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+75]['q_id']) , $("<td>").text(data[i+75]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+100]['q_id']) , $("<td>").text(data[i+100]['q_answer']));
                    if((i+125) < data.length ){
                        $tr3.append( $("<td>").text(data[i+125]['q_id']) , $("<td>").text(data[i+125]['q_answer']));
                    }
                    $('#qanswer1').append($tr3);
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i+150]['q_id']) , $("<td>").text(data[i+150]['q_answer']));
                    if((i+175) < data.length ){
                        $tr3.append( $("<td>").text(data[i+175]['q_id']) , $("<td>").text(data[i+175]['q_answer']));
                    }
                } else if ( data.length <= 225 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i]['q_id']) , $("<td>").text(data[i]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+25]['q_id']) , $("<td>").text(data[i+25]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+50]['q_id']) , $("<td>").text(data[i+50]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+75]['q_id']) , $("<td>").text(data[i+75]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+100]['q_id']) , $("<td>").text(data[i+100]['q_answer']));
                    if((i+125) < data.length ){
                        $tr3.append( $("<td>").text(data[i+125]['q_id']) , $("<td>").text(data[i+125]['q_answer']));
                    }
                    $('#qanswer1').append($tr3);
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i+150]['q_id']) , $("<td>").text(data[i+150]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+175]['q_id']) , $("<td>").text(data[i+175]['q_answer']));
                    if((i+200) < data.length ){
                        $tr3.append( $("<td>").text(data[i+200]['q_id']) , $("<td>").text(data[i+200]['q_answer']));
                    }
                } else if ( data.length <= 250 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i]['q_id']) , $("<td>").text(data[i]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+25]['q_id']) , $("<td>").text(data[i+25]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+50]['q_id']) , $("<td>").text(data[i+50]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+75]['q_id']) , $("<td>").text(data[i+75]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+100]['q_id']) , $("<td>").text(data[i+100]['q_answer']));
                    if((i+125) < data.length ){
                        $tr3.append( $("<td>").text(data[i+125]['q_id']) , $("<td>").text(data[i+125]['q_answer']));
                    }
                    $('#qanswer1').append($tr3);
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i+150]['q_id']) , $("<td>").text(data[i+150]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+175]['q_id']) , $("<td>").text(data[i+175]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+200]['q_id']) , $("<td>").text(data[i+200]['q_answer']));
                    if((i+225) < data.length ){
                        $tr3.append( $("<td>").text(data[i+225]['q_id']) , $("<td>").text(data[i+225]['q_answer']));
                    }
                } else if ( data.length <= 275 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i]['q_id']) , $("<td>").text(data[i]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+25]['q_id']) , $("<td>").text(data[i+25]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+50]['q_id']) , $("<td>").text(data[i+50]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+75]['q_id']) , $("<td>").text(data[i+75]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+100]['q_id']) , $("<td>").text(data[i+100]['q_answer']));
                    if((i+125) < data.length ){
                        $tr3.append( $("<td>").text(data[i+125]['q_id']) , $("<td>").text(data[i+125]['q_answer']));
                    }
                    $('#qanswer1').append($tr3);
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i+150]['q_id']) , $("<td>").text(data[i+150]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+175]['q_id']) , $("<td>").text(data[i+175]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+200]['q_id']) , $("<td>").text(data[i+200]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+225]['q_id']) , $("<td>").text(data[i+225]['q_answer']));
                    if((i+250) < data.length ){
                        $tr3.append( $("<td>").text(data[i+250]['q_id']) , $("<td>").text(data[i+250]['q_answer']));
                    }
                } else if ( data.length <= 300 ){
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i]['q_id']) , $("<td>").text(data[i]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+25]['q_id']) , $("<td>").text(data[i+25]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+50]['q_id']) , $("<td>").text(data[i+50]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+75]['q_id']) , $("<td>").text(data[i+75]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+100]['q_id']) , $("<td>").text(data[i+100]['q_answer']));
                    if((i+125) < data.length ){
                        $tr3.append( $("<td>").text(data[i+125]['q_id']) , $("<td>").text(data[i+125]['q_answer']));
                    }
                    $('#qanswer1').append($tr3);
                    $tr3 = $("<tr>");
                    $tr3.append( $("<td>").text(data[i+150]['q_id']) , $("<td>").text(data[i+150]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+175]['q_id']) , $("<td>").text(data[i+175]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+200]['q_id']) , $("<td>").text(data[i+200]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+225]['q_id']) , $("<td>").text(data[i+225]['q_answer']));
                    $tr3.append( $("<td>").text(data[i+250]['q_id']) , $("<td>").text(data[i+250]['q_answer']));
                    if((i+275) < data.length ){
                        $tr3.append( $("<td>").text(data[i+275]['q_id']) , $("<td>").text(data[i+275]['q_answer']));
                    }
                }
                $('#qanswer2').append($tr3);
            }

        }).fail( (data)=>{
            alert('fail');
        }).always( (data) => {

        });

    });

});