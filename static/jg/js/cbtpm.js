$(function(){
    var res_list = ["","ア","イ","ウ","エ","オ","カ","キ","ク","ケ","コ","サ","シ","ス","セ"];
    //JSONオブジェクトを文字列に変える
    function getJsonStr(json){
        return JSON.stringify(json);
    }

    //CSRF Tokenを取得する
    function getCSRFToken(){
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        return csrftoken;
    }

    //テストをクリック
    $('.q_q').on('click',function(){

        alert( dict['q_period']);

        var q_q = $(this).val();
        var json = {'q_test':$('#q_test').text() , 'q_period':$("#q_period").text(), 'q_q':q_q };
        $("#res").children().remove();

        $("#res").append( $('<p>').attr('id',q_q).text("問"+q_q));

        $.ajaxSetup({
            beforeSend : function(xhr,settings){
                xhr.setRequestHeader( 'X-CSRFToken',getCSRFToken());
            }
        });
        $.ajax({
            type:"POST",
            url:"/jg/ajax_cbtpm_get_q/",
            dataType:'json',
            contentType:'charset=utf-8',
            data:getJsonStr( json ),
        }).done( (data) => {
            var pdf = data['pdf'];
            $("#iframe").attr('src','/static/jg/pdf/question_pm/' + pdf + '#view=Fit');

            $old_question = data['list'][0]['q_question'];

            for( i = 0 ; i < data['list'].length ; i++){
                var q_question = data['list'][i]['q_question'];
                var q_symbol = data['list'][i]['q_symbol'];
                var q_lastanswer = data['list'][i]['q_lastanswer'];
                $p = $('<p>').attr('id',q_question);
                $label = $('<label>').text( q_symbol + ":" ).attr('for',q_question+q_symbol);
                $select = $('<select>').attr('id',q_question+q_symbol).attr('class','form-control').attr('style','width:100px');

                for( j = 0 ; res_list[j] != q_lastanswer ; j++ ){
                    $select.append( $('<option>').val(res_list[j]).text(res_list[j]));
                }
                $select.append( $('<option>').val(q_lastanswer).text(q_lastanswer) );
                $p.append( $label , $select );

                if( i == 0 || $old_question != q_question ){
                    $("#res").append( $('<p>').text("設問"+q_question));
                }

                $("#res").append( $p );
                $old_question = q_question;
            }
        }).fail((data)=>{

        }).always((data)=>{

        });
    });

});