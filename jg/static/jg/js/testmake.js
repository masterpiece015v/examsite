$(function(){
    var comp_list = [];
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

    //分類を取得するajax
    function ajax_getclass(child_class , query ){
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/jg/ajax_getclass/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            //全クリア
            $( child_class ).children().remove();
            $( child_class).append( $('<option>'));
            //追加
            Object.keys(data).forEach( function( key ){
                $option = $('<option>').val( key ).text( data[key] );
                $( child_class ).append( $option );
            });
        }).fail( (data)=>{
            alert( 'fail' );
        }).always( (data) => {
        });
    }

    //問題を取得するajax
    function ajax_getquestion( query ){
        var comp_list = [];
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/jg/ajax_getquestion/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#question').children().remove();

            for( var i = 0 , len=data.length; i<len;++i){
                $option = $('<option>').attr('value',data[i]['q_id']).text(data[i]['q_id'] + "," + data[i]['q_title']);
                $('#question').append( $option );
             }

             //問題数を表示
             $('#qcnt1').text( '問題数:' + $('#question option').length );

        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });
    }

    //テストごとの年度期を取得するajax
    function ajax_getperiod(child_class , query ){
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/jg/ajax_getperiod/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            //全クリア
            $( child_class ).children().remove();
            //追加
            for( var i = 0 , len=data.length; i<len;++i){
                //alert( data[i]['q_period']);
                $option = $('<option>').val( data[i]['q_period'] ).text( data[i]['q_period'] );
                $( child_class ).append( $option );
            }
        }).fail( (data)=>{
            alert( 'fail' );
        }).always( (data) => {
        });
    }

    function setModal( list_id ){
        $msq = $('#msq');
        $msq.children().remove();
        $listid = $( list_id );

        //モーダルに追加
        $listid.children().each(function(index,value){
            q_id = $(this).text().split(",")[0];
            $mtd = $("<td>")
            $p = $("<p>").text( $(this).val() + "," + $(this).text() );
            $img = $("<img src='" + '/static/jg/image/question/' + q_id + '.png' + "' style='width:400px;'>");
            $mtd.append( $p );
            $mtd.append( $img );
            //console.log('/static/exam/image/question/' + $(this).text() + '.png' );
            $mtr2 = $("<tr>").append( $mtd )
            $msq.append( $mtr2 )
        });


    }
    //ap,feの選択
    $("#q_test").on('change',function() {
        var json = {'q_test':$('#q_test').val() }
        //alert( json['q_test'] );
        ajax_getperiod('#q_period',json );
    });

    //大分類のリストのクリックイベント
    $("#l_class").on('click',function(){
        //大分類を選択すると中分類を取得する
        var json = {'l_class' : $('#l_class').val() }
        ajax_getclass( '#m_class' , json );
        //選択した大分類の問題を取得する
        var q_json = {'l_class':$('#l_class').val(), 'q_test':$('#q_test').val() }
        ajax_getquestion( q_json );
    });

    //中分類リストのクリックイベント
    $("#m_class").on('click',function(){
        //中分類を選択すると小分類を取得する
        var json = {"m_class" : $('#m_class').val()}
        ajax_getclass('#s_class', json);
        //選択した中分類の問題を取得する
        var q_json = {"l_class":$('#l_class').val() ,"m_class":$('#m_class').val(),"q_test":$('#q_test').val()}
        ajax_getquestion(q_json);
    });

    //小分類リストのクリックイベント
    $("#s_class").on('click',function(){
        //選択した小分類の問題を取得する
        var q_json = {"l_class":$('#l_class').val() ,"m_class":$('#m_class').val(),"s_class":$('#s_class').val(),"q_test":$('#q_test').val()}
        ajax_getquestion(q_json);
    });

    //問題選択ボタンのクリック
    $("#q_select").on('click',function(){
        $sq = $('#sq');
        $qua = $('#q_quantity');
        $sq.children().remove();
        var max = $('#a_que').children().length;
        var num = $qua.val();
        console.log( num );
        if( num == 0 ){
            //すべて追加
            cnt = 1;
            $("#a_que").children().each(function(){
                $option = $('<option>');
                code4 = getcode4( cnt );
                $option.attr('value',code4);
                $option.text( $(this).text() );
                $sq.append( $option );

                cnt = cnt + 1;
            });
            $('#qcnt2').text( "問題数:" + $("#sq").children().length );
            //モーダルモードに追加
            setModal("#sq");

        }else{
            //問題数が選択問題数を超えているかチェック
            if( max >= num ){
                //排他的ランダム数を取得するジェネリック
                var gen = getrandom(max)
                for( var i = 1 ; i <= num ; i++){
                    code4 = getcode4( i );
                    $opt = $("#a_que option:nth-child(" + gen.next().value + ")");
                    $option = $('<option>').attr('value',code4).text( $opt.text() );
                    $sq.append( $option );

                }
                //console.log( num );
                $('#qcnt2').text( '問題数:' + num );
                setModal("#sq");
            }else{
                alert( '問題数が足りません。');
            }
        }
    });

    $('#a_que').on('dblclick',function(){
        a_que_val = $(this).val();
        text = $(this).children('[value=' + a_que_val +']').text();

        value = getcode4( $('#sq').children().length + 1 );

        $('#sq').append( $('<option>').val(value).text( text ));

        $("#qcnt2").text( "テスト問題数:" + $("#sq").children().length );

        $("#sq").children().each( function(index,value){

            console.log( $(this).val() );
            console.log( $(this).text() );
        });

        setModal("#sq");
    });
    //問題にするリストをダブルクリック
    $('#question').on('dblclick',function(){
        //var txt = $('#a_que option:selected').text();
        //alert( txt );
        value = $(this).val();
        $(this).children('[value=' + value + ']').remove();

        //$(this).children().each(function(index,value){
            //$('#sq').append( $('<option>').val(getcode4(index+1)).text(value.text));
            //$(this).remove();
            //value.val = getcode4(index+1);
            //console.log( value.text );
        //});

        $("#qcnt1").text( "テスト問題数:" + $(this).children().length );
        //setModal("#sq");
    });
    //問題にするリストをダブルクリック
    $('#sq').on('dblclick',function(){
        //var txt = $('#a_que option:selected').text();
        //alert( txt );
        value = $(this).val();
        $(this).children('[value=' + value + ']').remove();

        $(this).children().each(function(index,value){
            $('#sq').append( $('<option>').val(getcode4(index+1)).text(value.text));
            $(this).remove();
            //value.val = getcode4(index+1);
            //console.log( value.text );
        });

        $("#qcnt2").text( "テスト問題数:" + $(this).children().length );
        setModal("#sq");
    });

    //問題の追加
    $("#q_add").on('click',function(){
        $('#question').children().each(function(){
            $("#a_que").append( $(this) );
        });
        $('#a_qcnt').text( "問題数:" + $("#a_que").children().length );
    });
    //問題の新規
    $("#q_renew").on('click',function(){
        $("#a_que").children().remove();
        $('#question').children().each(function(){
            $("#a_que").append( $(this) );
        });
        $('#a_qcnt').text( "問題数:" + $("#a_que").children().length );
    });

    //テストの作成
    $("#q_make").on('click',function(){
        var q_json = {}
        //q_json['chadd'] = $('#chadd').val();
        q_json['q_test'] = $('#q_test').val();
        //console.log( q_json['chadd'] );
        console.log( q_json['q_test']);

        if ( $('#l_class').val() !== null){
            q_json['l_class'] = $('#l_class').val();
        }
        if ( $('#m_class').val() !== null){
            q_json['m_class'] = $('#m_class').val();
        }
        if( $('#s_class').val() !== null){
            q_json['s_class'] = $('#s_class').val();
        }

        var q_list = [];
        cnt = 1;
        $('#sq').children().each(function(){
            var data = {};
            data['t_num'] = $(this).val();

            text = $(this).text();

            q_id = text.split(',')[0];
            data['q_id'] = q_id;

            console.log( data['t_num'] );
            console.log( data['q_id'] );
            q_list.push( data );
        });

        q_json['q_list'] = q_list;

        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/jg/ajax_testupdate/",
            dataType:'json',
            data: getJsonStr( q_json ),
            contentType: 'charset=utf-8'

        }).done( (data) => {

            $('#modal-progress').modal('hide');

        }).fail( (data)=>{
            alert('error');
        }).always( (data) => {
        });

    });

    //フィルタボタン
    $("#q_filter_button").on('click',function(){
        pattern = $("#q_filter_text").val();
        $('#question').children().each(function(){
            source = $(this).val();
            if( source.indexOf(pattern)===0){
                console.log( $(this).val() );
            }else{
                $(this).remove();
            }
        });
        $('#qcnt1').text( "問題数:" + $("#question").children().length );
    });
});
