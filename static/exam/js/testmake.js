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
            url:"/exam/getclass/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            //全クリア
            $( child_class ).children().remove();
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
            url:"/exam/getquestion/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#question').children().remove();

            for( var i = 0 , len=data.length; i<len;++i){

                //code4 = getcode4(i+1);
                //select ver

                $option = $('<option>').attr('value',data[i]['q_id']).text(data[i]['q_id'] + "," + data[i]['q_title']);
                $('#question').append( $option );

                //table ver
                /*
                $tr = $("<tr id='tr" + code4 + "'>");
                $td = $('<td>').text( code4 );
                $tr.append( $td );
                $td = $('<td>').text( data[i]['q_id'] );
                $tr.append( $td );
                $td = $('<td>').text( data[i]['q_title']);
                $tr.append( $td );
                $('#question').append( $tr );
                */
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
            url:"/exam/getperiod/",
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

    //年度期リストのクリックイベント
    $("#q_period").on('click',function(){
        //選択した年度期の問題を取得する
        var q_json={"q_test":$('#q_test').val(),"q_period":$('#q_period').val()}
        ajax_getquestion( q_json );
    });

    //問題選択ボタンのクリック
    $("#q_select").on('click',function(){
        $sq = $('#sq');
        $msq = $('#msq');
        $qua = $('#q_quantity');
        $sq.children().remove();
        $msq.children().remove();
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
                //モーダルに追加
                $mtd = $("<td>")
                $img = $("<img src='" + '/static/exam/image/question/' + $(this).attr('value') + '.png' + "'>");
                $mtd.append( $img );
                //console.log('/static/exam/image/question/' + $(this).text() + '.png' );
                $mtr2 = $("<tr>").append( $mtd )
                $msq.append( $mtr2 )

                cnt = cnt + 1;
            });
            $('#qcnt2').text( "問題数:" + $("#sq").children().length );
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
                    //ランダムに選ばれた問題に追加
                    //$dtr = $("<tr id='" + code4 + "'>");
                    //$td1 = $('<td>').text( code4 );
                    //$dtr.append( $td1 );

                    //モダールに追加
                    $mtr1 = $("<tr id='" + code4 + "'>");
                    $mtd1 = $('<td>').text( code4 );
                    $mtr1.append( $mtd1 );
                    $mtd2 = $("<td>")
                    $img = $("<img src='" + '/static/exam/image/question/' + $opt.attr('value') + '.png' + "' style='width:400px;'>");
                    $mtd2.append( $img );
                    $mtr1.append( $mtd2);

                    $('#msq').append( $mtr1 );

                }
                //console.log( num );
                $('#qcnt2').text( '問題数:' + num );
            }else{
                alert( '問題数が足りません。');
            }
        }
    });

    //ダブルクリック
    $('#a_que').on('dblclick',function(){
        //var txt = $('#a_que option:selected').text();
        //alert( txt );
        alert('dblclick');
    });

    //問題選択ボタンのクリック
    //table ver
    /*
    $("#q_select").on('click',function(){
        $('#sq').children().remove();
        $('#msq').children().remove();
        $q_qua = $('#q_quantity');

        var max = $('#a_que').children().length;
        var num = $q_qua.val();

        //全てを追加する
        if( num == 0 ){
            $('#a_que').children().each(function(){
                $tr = $("<tr id='" + $(this).id + "'>");
                $option = $('<option>');
                cnt = 0;
                $(this).children().each(function(){
                    $td = $('<td>').text( $(this).text() );
                    $tr.append( $td );
                    if(cnt==0){
                        $mtr1 = $("<tr>");
                        $mtd = $('<td>').text( $(this).text() );
                        $mtr1.append( $mtd );
                        $('#msq').append( $mtr1 );
                    }
                    if(cnt == 1){
                        $mtd = $("<td>")
                        $img = $("<img src='" + '/static/exam/image/question/' + $(this).text() + '.png' + "'>");
                        $mtd.append( $img );
                        //console.log('/static/exam/image/question/' + $(this).text() + '.png' );
                        $mtr2 = $("<tr>").append( $mtd )
                        $('#msq').append( $mtr2 );
                    }
                    cnt = cnt + 1;
                });
                $('#sq').append( $tr );
            });
            $('#qcnt2').text( "問題数:" + $("#sq").children().length );
        }else{
            //問題数が選択問題数を超えているかチェック
            if( max >= num ){
                //排他的ランダム数を取得するジェネリック
                var gen = getrandom(max)
                for( var i = 1 ; i <= num ; i++){

                    code4 = getcode4( i );
                    $str = $('#a_que tr:nth-child(' + gen.next().value + ')');
                    //ランダムに選ばれた問題に追加
                    $dtr = $("<tr id='" + code4 + "'>");
                    $td1 = $('<td>').text( code4 );
                    $dtr.append( $td1 );

                    //モダールに追加
                    $mtr1 = $("<tr id='" + code4 + "'>");
                    $mtd1 = $('<td>').text( code4 );
                    $mtr1.append( $mtd1 );

                    $('#msq').append( $mtr1 );
                    cnt = 0;
                    $str.children().each(function(){
                        if(cnt > 0){
                            $td = $('<td>').text( $(this).text() );
                            $dtr.append( $td );
                        }
                        if(cnt == 1){
                            $mtd2 = $("<td>")
                            $img = $("<img src='" + '/static/exam/image/question/' + $(this).text() + '.png' + "' style='width:400px;'>");
                            $mtd2.append( $img );
                            //console.log('/static/exam/image/question/' + $(this).text() + '.png' );
                            $mtr2 = $("<tr>").append( $mtd2 )
                            $('#msq').append( $mtr2 );
                        }
                        cnt = cnt + 1;
                    });

                    $('#sq').append( $dtr );

                }
                //console.log( num );
                $('#qcnt2').text( '問題数:' + num );
            }else{
                alert( '問題数が足りません。');
            }
        }
    });
    */
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

    //table ver
    /*
    $("#q_add").on('click',function(){
        $('#question').children().each(function(){
            $tr = $("<tr id='" + $(this).attr('id') + "' class='tr1'>");
            var cnt = 0;
            $(this).children().each(function(){
                $td = $('<td>').text( $(this).text() );
                $tr.append( $td );
                if(cnt==0){
                    $mtr1 = $("<tr>");
                    $mtd = $('<td>').text( $(this).text() );
                    $mtr1.append( $mtd );
                    $('#msq').append( $mtr1 );
                }
                if(cnt == 1){
                    $mtd = $("<td>")
                    $img = $("<img src='" + '/static/exam/image/question/' + $(this).text() + '.png' + "'>");
                    $mtd.append( $img );
                    //console.log('/static/exam/image/question/' + $(this).text() + '.png' );
                    $mtr2 = $("<tr>").append( $mtd )
                    $('#msq').append( $mtr2 );
                }
                cnt = cnt + 1;
            });
            $('#a_que').append( $tr );
        });
        $('#a_qcnt').text( "問題数:" + $("#a_que").children().length );
    });
    */
    //問題の新規
    //table ver
    /*
    $("#q_renew").on('click',function(){
        $('#a_que').children().remove();
        $('#msq').children().remove();

        $('#question').children().each(function(){
            $tr = $("<tr id='" + $(this).attr('id') + "' class='tr1'>");
            var cnt = 0;
            $(this).children().each(function(){
                $td = $('<td>').text( $(this).text() );
                $tr.append( $td );
                if(cnt==0){
                    $mtr1 = $("<tr>");
                    $mtd = $('<td>').text( $(this).text() );
                    $mtr1.append( $mtd );
                    $('#msq').append( $mtr1 );
                }
                if(cnt == 1){
                    $mtd = $("<td>")
                    $img = $("<img src='" + '/static/exam/image/question/' + $(this).text() + '.png' + "'>");
                    $mtd.append( $img );
                    //console.log('/static/exam/image/question/' + $(this).text() + '.png' );
                    $mtr2 = $("<tr>").append( $mtd )
                    $('#msq').append( $mtr2 );
                }
                cnt = cnt + 1;
            });
            $('#a_que').append( $tr );
        });
        $('#a_qcnt').text( "問題数:" + $("#a_que").children().length );
    });
    */

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
            url:"/exam/testupdate/",
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

    //テストの作成
    $("#q_make_period").on('click',function(){
        var q_json = {}
        q_json['chadd'] = $('#chadd').val();
        q_json['q_test'] = $('#q_test').val();
        console.log( q_json['chadd'] );
        console.log( q_json['q_test']);

        var q_list = [];

        $('#question').children().each(function(){
            var data = {};
            cnt = 1;
            $(this).children().each(function(){
                switch( cnt ){
                    case 1:
                        data['t_num'] = $(this).text();
                        break;
                    case 2:
                        data['q_id'] = $(this).text();
                        break;
                    case 3:
                }
                cnt = cnt + 1;
            });
            console.log( data );
            q_list.push( data );
        });

        q_json['q_list'] = q_list;

        //console.log( q_list );

        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/exam/testupdate/",
            dataType:'json',
            data: getJsonStr( q_json ),
            contentType: 'charset=utf-8'

        }).done( (data) => {

            $('#modal-progress').modal('hide');

        }).fail( (data)=>{
        }).always( (data) => {
        });
    });

});