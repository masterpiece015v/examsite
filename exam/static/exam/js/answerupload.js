$(function(){
    //ファイルを変更したときの処理
    $(document).on('change', ':file', function() {
        var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
        input.parent().parent().next(':text').val(label);
    });

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
    function ajax_getresult(child_class, query ){

        console.log( getJsonStr(query) );

        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/exam/ajax_answerupload/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {

            $(child_class).children().remove();
            $('msg').text = data['message'];

            //console.log( data );

            /*
            for( var i = 0 , len=data['t_num'].length; i<len;++i){
                code4 = getcode4(i+1);
                $tr = $("<tr id='tr" + code4 + "'>");
                //Object.keys(data[i]).forEach( function( key ){
                //    $td = $('<td>').text( data[i][key] );
                //    $tr.append( $td );
                //});
                $td = $('<td>').text( data['t_num'][i]);
                $tr.append( $td );
                $td = $("<td>").text( data['q_id'][i]);
                $tr.append( $td );
                $td = $('<td>').text( data['r_answer'][i]);
                $tr.append( $td );
                $td = $('<td>').text( data['q_answer'][i]);
                $tr.append( $td );
                $td = $('<td>').text( data['mb'][i])
                if( data['mb'][i]=='0'){
                    $tr.attr('style','background-color:red;color:white;')
                }
                $tr.append( $td );

                $('#resultdata').append( $tr );

            }
            */
        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });
    }

    //ユーザのリストをクリック
    $("#btn_upload").on('click',function(){
        //ユーザのidを送信する
        var items = [];
        var flg = 0;
        $("#answer_table tr").each(function(i){
            //var item = [$(this).cells(0) ,$(this).eq(2).text()];
            //items.push( item );
            var item = [];
            $(this).children().each(function(i){
                if( i == 0 ){

                    item.push( $(this).text() );
                    //console.log( $(this).text() );
                }else{
                    item.push( $(this).children('input').val() );
                    //console.log( $(this).children('input').val());
                }
            });
            items.push( item );
        });

        var json = {'t_id':$('#t_id').val(),'u_id':$("#u_id").val() , 'answerlist':items };

        ajax_getresult( '#answer_table' , json );
    });


});