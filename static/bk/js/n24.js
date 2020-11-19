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

        var query = {'b_field':$(this).val() };

        $("#t_id").text( "テストID:" + query['b_field'] );

        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/bk/ajax_n24_gettimes/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            //$('#b_times').children().remove();
            //$('#b_times').append( $('<option>') );
            //for( var i = 0 ;  i < data.qlist.length ; i++){
            //    console.log( i );
            //    $option = $('<option>').val(data.qlist[i]['b_times']).text(data.qlist[i]['b_times']);
            //    $('#b_times').append( $option );
            //}
            $('#printlist').children().remove();
            $('#qtable').children().remove();
            for( var i = 0 ; i < data.qlist.length ; i++ ){
                $tr = $('<tr>');
                $td1 = $("<td width='50px'>").text( data.qlist[i]['b_times'] );
                $td3 = $("<td>").text( data.qlist[i]['b_ocr']);
                $td2 = $("<td width='30px'>").append( $('<input>').attr('type','checkbox').attr('name','chktimes').val(data.qlist[i]['b_times']) );
                $tr.append( $td1 );
                $tr.append( $td2 );
                $tr.append( $td3 );
                $('#printlist').append( $tr );
            }



        }).fail( (data)=>{
            alert('fail');
        }).always( (data) => {

        });

    });
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
    //回の選択
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
        console.log( getJsonStr( query ) );

        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/bk/ajax_n24_getquestion/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#qtable').children().remove();
            console.log( data.qlist );
            for( var i = 0 ;  i < data.qlist.length ; i++){
                for( var j = 0 ; j < data.qlist[i].list.length ; j++ ){
                    $p = $('<p>').text("第" + data.qlist[i]['b_times'] + "回 問" + data.qlist[i].list[j].b_que1 );
                    $p.attr("style","font-size:14pt;");

                    $img = $("<img src='/static/bk/question/" + data.qlist[i].list[j].b_id + ".png'>");
                    $img.attr("style","width:900px;");
                    $img.attr("class","q_img");
                    $figure = $('<figure>').append($img);

                    $('#qtable').append( $p );
                    $('#qtable').append( $figure );
                }
            }
            $('#qtable').append( $("<div>").attr("style","page-break-after: always"));
            //解答用紙
            for( var i = 0 ; i < data.qlist.length ; i++ ){
                as_page = data.qlist[i].list[0].b_as_page;
                console.log( as_page );
                filename = "n_" + data.qlist[i].b_times + "_2_4_";
                $p = $('<p>').text("第" + data.qlist[i].b_times + "回 問" + data.qlist[i].list[0].b_que1 + "【解答用紙】");
                $p.attr("style","font-size:14pt");
                $('#qtable').append( $p );
                for( var j = 0 ; j < as_page ; j++ ){
                    $img = $("<img src='/static/bk/question/" + filename + (j+1) + "_as.png'>" );
                    $img.attr("style","width:900px;");
                    $img.attr("class","q_img");
                    $figure = $('<figure>').append($img);
                    $('#qtable').append( $p );
                    $('#qtable').append( $figure );

                }
            }
            $('#qtable').append( $("<div>").attr("style","page-break-after: always"));
            //解答
            for( var i = 0 ; i < data.qlist.length ; i++ ){
                ans_page = data.qlist[i].list[0].b_ans_page;
                filename = "n_" + data.qlist[i].b_times + "_2_4_";
                $p = $('<p>').text("第" + data.qlist[i].b_times + "回 問" + data.qlist[i].list[0].b_que1 + "【解答】");
                $p.attr("style","font-size:14pt");
                $('#qtable').append( $p );
                for( var j = 0 ; j < ans_page ; j++ ){

                    $img = $("<img src='/static/bk/question/" + filename + (j+1) + "_ans.png'>" );
                    $img.attr("style","width:900px;");
                    $img.attr("class","q_img");
                    $figure = $('<figure>').append($img);
                    $('#qtable').append( $p );
                    $('#qtable').append( $figure );

                }
            }
            $('#qtable').append( $("<div>").attr("style","page-break-after: always"));
            //解説
            for( var i = 0 ; i < data.qlist.length ; i++ ){
                com_page = data.qlist[i].list[0].b_com_page;
                filename = "n_" + data.qlist[i].b_times + "_2_4_";
                $p = $('<p>').text("第" + data.qlist[i].b_times + "回 問" + data.qlist[i].list[0].b_que1 + "【解説】");
                $p.attr("style","font-size:14pt");
                $('#qtable').append( $p );
                for( var j = 0 ; j < com_page ; j++ ){

                    $img = $("<img src='/static/bk/question/" + filename + (j+1) + "_com.png'>" );
                    $img.attr("style","width:900px;");
                    $img.attr("class","q_img");
                    $figure = $('<figure>').append($img);
                    $('#qtable').append( $p );
                    $('#qtable').append( $figure );

                }
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