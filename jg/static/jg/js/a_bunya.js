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

    //問題を取得するajax
    function ajax_getresult2(child_class, query ){
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });
        $.ajax({
            type:"POST",
            url:"/jg/ajax_getresultbunya/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {

            count = 0;
            resultcount = 0;

            // １件目は入れておく
            //モーダル
            modalid = data[0]['m_id'] + data[0]['s_id'];
            $modal_main = $('#modal');
            $modal_main.children().remove();
            $modal = $('<div>').attr('id',modalid).attr('class','modal js-modal');
            $modal.append( $('<div>').attr('class','modal__bg js-modal-close'));
            $modal_content = $('<div>').attr('class','modal__content');
            $modal_content.append( $('<a href="">').attr('class','js-modal-close').text('閉じる'));

            $modal_item = $("<div style='padding:5px;margin-top:20px;border-top:solid 2px black;'>");
            if( data[0]['result']==0){
                //間違っていたら背景を赤にする
                $modal_item = $modal_item.attr('style','padding:5px;margin-top:20px;border-top:solid 2px black;background-color:red');
            }
            $modal_item.append( $("<p style='margin-top:5px;'>").text(data[0]['q_id']) );
            $modal_item.append( $("<p style='margin-top:5px;'>").append($("<img src='/static/jg/image/question/" + data[0]['q_id'] + ".png' alt='" + data[0]['q_id'] + "' style='width:600px'>" )));
            $modal_answer = $( "<p style='margin-top:5px;'>" );
            $modal_answer.append( $("<span>").text("あなたの解答:") );
            $modal_answer.append( $("<span class='r_answer'>").text( data[0]['r_answer']) );
            $modal_answer.append( $("<span>").text("答え:"));
            $modal_answer.append( $("<span class='q_answer'>").text( data[0]['q_answer']));
            $modal_item.append( $modal_answer );
            $modal_content.append( $modal_item );

            //　テーブル
            $r = $('#resultdata')
            $r.children().remove();
            old_s_name = data[0]['s_name'];
            old_m_name = data[0]['m_name'];
            old_l_name = data[0]['l_name']

            for( var i = 1 , len=data.length ; i<len ; ++i ){
                if( old_s_name != data[i]['s_name'] ){
                    $modal_content.append( $modal_item );
                    $modal.append( $modal_content );
                    $modal_main.append( $modal );
                    $tr = $('<tr>');
                    $td1 = $('<td>').text(old_l_name );
                    $td2 = $('<td>').text(old_m_name );
                    $td3 = $('<td>').append( $('<a href="">').attr('class','js-modal-open').attr('data-target',modalid).text( old_s_name ));
                    $td4 = $('<td>').text( resultcount );
                    $td5 = $('<td>').text(count);
                    $td6 = $('<td>').text( Math.round( (resultcount /count ) *100) / 100 );
                    $tr.append( $td1,$td2,$td3,$td4,$td5,$td6 );
                    $r.append( $tr );
                    old_l_name = data[i]['l_name'];
                    old_m_name = data[i]['m_name'];
                    old_s_name = data[i]['s_name'];

                    //モーダルに追加
                    modalid = data[i]['m_id'] + data[i]['s_id'];
                    $modal = $('<div>').attr('id',modalid).attr('class','modal js-modal');
                    $modal.append( $('<div>').attr('class','modal__bg js-modal-close'));
                    $modal_content = $('<div>').attr('class','modal__content');
                    $modal_content.append( $('<a href="">').attr('class','js-modal-close').text('閉じる'));
                    $modal_item = $("<div style='padding:5px;margin-top:20px;border-top:solid 2px black;'>");
                    if( data[i]['result']==0){
                        $modal_item = $modal_item.attr('style','padding:5px;margin-top:20px;border-top:solid 2px black;background-color:red');
                    }
                    $modal_item.append( $("<p style='margin-top:5px;'>").text(data[i]['q_id']) );
                    $modal_item.append( $("<p style='margin-top:5px;'>").append($("<img src='/static/jg/image/question/" + data[i]['q_id'] + ".png' alt='" + data[i]['q_id'] + "' style='width:600px'>" )));
                    $modal_answer = $( "<p style='margin-top:5px;'>" );
                    $modal_answer.append( $("<span>").text("あなたの解答:") );
                    $modal_answer.append( $("<span class='r_answer'>").text( data[i]['r_answer']) );
                    $modal_answer.append( $("<span>").text("  答え:"));
                    $modal_answer.append( $("<span class='q_answer'>").text( data[i]['q_answer']));
                    $modal_item.append( $modal_answer );
                    $modal_content.append( $modal_item );
                    count = 1;
                    resultcount = data[i]['result'];
                }else{
                    $modal_item = $("<div style='padding:5px;margin-top:20px;border-top:solid 2px black;'>");
                    if( data[i]['result']==0){
                        $modal_item = $modal_item.attr('style','padding:5px;margin-top:20px;border-top:solid 2px black;background-color:red');
                    }
                    $modal_item.append( $("<p style='margin-top:5px;'>").text(data[i]['q_id']) );
                    $modal_item.append( $("<p style='margin-top:5px;'>").append($("<img src='/static/jg/image/question/" + data[i]['q_id'] + ".png' alt='" + data[i]['q_id'] + "' style='width:600px'>" )));
                    $modal_answer = $("<p style='margin-top:5px;'>");
                    $modal_answer.append( $("<span>").text("あなたの解答:") );
                    $modal_answer.append( $("<span class='r_answer'>").text( data[i]['r_answer']) );
                    $modal_answer.append( $("<span>").text("答え:"));
                    $modal_answer.append( $("<span class='q_answer'>").text( data[i]['q_answer']));
                    $modal_item.append( $modal_answer );
                    $modal_content.append( $modal_item );

                    count++;
                    resultcount = resultcount + data[i]['result'];
                }
            }

            modalset();

        }).fail( (data)=>{
            alert( data );
        }).always( (data) => {
        });
    }
    //ダウンリスト
    $("#resultdata dt").on("click", function() {
        $("#resultdata div").slideToggle();
    });
    //ユーザのリストをクリック
    $("#lst_user").on('click',function(){
        //ユーザのidを送信する
        var json = {'u_id' : $('#lst_user').val() };
        ajax_getresult2( '#lst_tid' , json );
    });
    $("#showdata").on('click',function(){
        //ユーザのidを送信する
        var json = {'u_id' : $('#u_id').text() };
        ajax_getresult2( '#resultdata' , json );
    });
    //モダールのイベント
    function modalset(){
        $('.js-modal-open').each(function(){
            $(this).on('click',function(){
                var target = $(this).data('target');
                var modal = document.getElementById(target);
                $(modal).fadeIn();
                return false;
            });
        });
        $('.js-modal-close').on('click',function(){
            $('.js-modal').fadeOut();
            return false;
        });
    }
});
