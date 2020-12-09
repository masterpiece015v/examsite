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

    //分野の選択
    $("#s_test").on('change',function(){
        getitem( 1 );
    });
    $('#field2').on('change',function(){
        getitem( 2 );
    });
    $('#field3').on('change',function(){
        getitem( 3 );
    });
    //分野の選択関数
    function getitem( flg ){

        $s_test = $('#s_test');
        $field2 = $('#field2');
        $field3 = $('#field3');

        var query = {};

        if( $field3.val().length > 0 ){
            query['b_field'] = $s_test.val();
            query['b_field2'] = $field2.val();
            query['b_field3'] = $field3.val();
        }else if($field2.val().length > 0 ){
            query['b_field'] = $s_test.val();
            query['b_field2'] = $field2.val();
        }else{
            query['b_field'] = $s_test.val();
        }

        console.log( query );

        $("#t_id").text( "テストID:" + query['b_field'] );

        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/bk/ajax_n21_gettimes/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#printlist').children().remove();
            $('#qtable').children().remove();
            $('#allow_field').children().remove();

            if( flg == 1 ){
                item2 = $('#field2').val();
                $('#field2').children().remove();
                $('#field2').append( $('<option>') );
                for( var i = 0 ; i < data.field2.length ; i++ ){
                    if( item2 == data.field2[i] ){
                        $option = $('<option>').text( data.field2[i] ).val( data.field2[i] ).prop('selected',true);
                    }else{
                        $option = $('<option>').text( data.field2[i] ).val( data.field2[i] );
                    }
                    $('#field2').append( $option );
                }
                item3 = $('#field3').val();
                $('#field3').children().remove();
                $('#field3').append( $('<option>') );
                for( var i = 0 ; i < data.field3.length ; i++ ){
                    if( item3 == data.field3[i] ){
                        $option = $('<option>').text( data.field3[i] ).val( data.field3[i] ).prop('selected',true);
                    }else{
                        $option = $('<option>').text( data.field3[i] ).val( data.field3[i] );
                    }
                    $('#field3').append( $option );
                }
            }else if( flg == 2 ){
                item3 = $('#field3').val();
                $('#field3').children().remove();
                $('#field3').append( $('<option>') );
                for( var i = 0 ; i < data.field3.length ; i++ ){
                    if( item3 == data.field3[i] ){
                        $option = $('<option>').text( data.field3[i] ).val( data.field3[i] ).prop('selected',true);
                    }else{
                        $option = $('<option>').text( data.field3[i] ).val( data.field3[i] );
                    }
                    $('#field3').append( $option );
                }
            }

            for( var i = 0 ; i < data.qlist.length ; i++ ){
                $tr = $('<tr>');
                $td1 = $("<td width='50px'>").text( data.qlist[i]['b_times'] );
                $td4 = $("<td width='50px'>").text( '(' + data.qlist[i]['b_que2'] + ')' );
                $td3 = $("<td>").text( data.qlist[i]['b_ocr']);
                $td2 = $("<td width='30px'>").append( $('<input>').attr('type','checkbox').attr('name','chktimes').val(data.qlist[i]['b_times'] + '_1_' + data.qlist[i]['b_que2']) );
                $tr.append( $td1 );
                $tr.append( $td4 );
                $tr.append( $td2 );
                $tr.append( $td3 );
                $('#printlist').append( $tr );
            }

        }).fail( (data)=>{
            alert('fail');
        }).always( (data) => {

        });
    }
    //すべてのチェックを入れる
    $('#chkon').on('click',function(){
        $('input[type=checkbox]').each( function(index){
            $(this).prop('checked',true);
        });
    });
    //すべてのチェックを入れる
    $('#chkoff').on('click',function(){
        $('input[type=checkbox]').each( function(index){
            $(this).prop('checked',false);
        });
    });
    //印刷表示ボタンクリック
    $("#print").on('click',function(){
        var array = [];
        $('input[type=checkbox]').each( function(index){
            if( $(this).prop('checked') ){
                array.push( $(this).val() );
            }else{

            }
        });
        var query={};
        query['b_times'] = array;
        //console.log( getJsonStr( query ) );
        query['b_field'] = $('#s_test').val()
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
            $('#allow_field').children().remove();
            //問題の表示
            for( var i = 0 ;  i < data.qlist.length ; i++){
                qlist = data.qlist[i];
                $p = $('<p>').text("第" +qlist['b_times'] + "回 問" + qlist.b_que1 + '(' + qlist.b_que2 + ') 分野:' + qlist['b_field']);
                $p.attr("style","font-size:14pt;border-top:solid 1px black");

                $table = $('<table>').attr('style','margin:10px;width:800px;text-align:center;').append( $('<caption>').attr('style','caption-side:top').text('許容勘定科目'));
                $tr = $('<tr>');
                b_allow_field = qlist.b_allow_field;
                $td = $('<td>').text( b_allow_field[0] );
                $tr.append( $td );

                for( var j = 1 ; j < b_allow_field.length ; j++ ){
                    if( j % 5 == 0 ){
                        $table.append( $tr );
                        $tr = $('<tr>');
                        $td = $('<td>').text( b_allow_field[j] );
                        $tr.append( $td );
                    }else{
                        $td = $('<td>').text( b_allow_field[j] );
                        $tr.append( $td );
                    }
                }
                $table.append( $tr );



                $img = $("<img src='/static/bk/question/" + data.qlist[i].b_id + ".png'>");
                $img.attr("style","width:900px;");
                $img.attr("class","q_img");
                $figure = $('<figure>').append($img);

                $('#qtable').append( $p );
                $('#qtable').append( $table );
                $('#qtable').append( $figure );
            }
            $('#qtable').append( $("<div>").attr("style","page-break-after: always"));

            //解答用紙
            $tableas = $("<table>");
            for( var i = 0 ; i < data.qlist.length ; i++ ){
                $tr1 = $("<tr>");
                $th = $("<th colspan=4>").text( "第" + data.qlist[i].b_times + "回 問" + data.qlist[i].b_que1 + '(' + data.qlist[i].b_que2 + ')' + "【解答用紙】" );
                $tr1.append( $th );

                $tr2 = $("<tr>");
                $td1 = $("<td>").attr('style','border:1px solid black;width:250px;height:150px;');
                $td2 = $("<td>").attr('style','border:1px solid black;width:250px;height:150px;');
                $td3 = $("<td>").attr('style','border:1px solid black;width:250px;height:150px;');
                $td4 = $("<td>").attr('style','border:1px solid black;width:250px;height:150px;');
                $tr2.append( $td1,$td2,$td3,$td4 );

                $tableas.append( $tr1,$tr2 );
            }
            $('#qtable').append( $tableas );
            $('#qtable').append( $("<div>").attr("style","page-break-after: always"));
            //解答
            for( var i = 0 ; i < data.qlist.length ; i++ ){
                filename = "n_" + data.qlist[i].b_times + "_2_1_";
                $p = $('<p>').text("第" + data.qlist[i].b_times + "回 問" + data.qlist[i].b_que1 + '(' + data.qlist[i].b_que2 + ')' + "【解答】");
                $p.attr("style","font-size:14pt");
                $('#qtable').append( $p );
                $img = $("<img src='/static/bk/question/" + filename + data.qlist[i].b_que2 + "_ans.png'>" );
                $img.attr("style","width:900px;");
                $img.attr("class","q_img");
                $figure = $('<figure>').append($img);
                $('#qtable').append( $p );
                $('#qtable').append( $figure );
            }

            $('#qtable').append( $("<div>").attr("style","page-break-after: always"));
            //解説
            for( var i = 0 ; i < data.qlist.length ; i++ ){
                filename = "n_" + data.qlist[i].b_times + "_2_1_";
                $p = $('<p>').text("第" + data.qlist[i].b_times + "回 問" + data.qlist[i].b_que1 + '(' + data.qlist[i].b_que2 + ')' + "【解説】");
                $p.attr("style","font-size:14pt");
                $('#qtable').append( $p );
                $img = $("<img src='/static/bk/question/" + filename + data.qlist[i].b_que2 + "_com.png'>" );
                $img.attr("style","width:900px;");
                $img.attr("class","q_img");
                $figure = $('<figure>').append($img);
                $('#qtable').append( $p );
                $('#qtable').append( $figure );
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