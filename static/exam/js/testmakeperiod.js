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
            url:"/exam/ajax_getquestion/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#question').children().remove();

            for( var i = 0 , len=data.length; i<len;++i){
                $tr = $('<tr>');
                $tr.append( $('<td>').text(data[i]['q_id']) );
                $tr.append( $('<td>').text(data[i]['q_title']) );
                $('#question').append( $tr );
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
            url:"/exam/ajax_getperiod/",
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

    //年度期リストのクリックイベント
    $("#q_period").on('click',function(){
        //選択した年度期の問題を取得する
        var q_json={"q_test":$('#q_test').val(),"q_period":$('#q_period').val()}
        ajax_getquestion( q_json );
    });

    //テストの作成
    $("#q_make_period").on('click',function(){
        var q_json = {}

        var q_list = [];

        $('#question').children().each(function(index , value){
            t_num = getcode4( index + 1);
            q_id = $( $(value).children()[0] ).text();
            data = {};
            data['t_num'] = t_num;
            data['q_id'] = q_id;
            q_list.push( data );
        });

        q_json['q_list'] = q_list;

        //console.log( q_list );

        ajax_testupdate(q_json);
    });

    function ajax_testupdate(q_json){
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/exam/ajax_testupdateperiod/",
            dataType:'json',
            data: getJsonStr( q_json ),
            contentType: 'charset=utf-8'

        }).done( (data) => {

            $('#modal-progress').modal('hide');

        }).fail( (data)=>{
        }).always( (data) => {
        });
    }
});
