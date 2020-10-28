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

    //基本、応用の切り替え
    $("#test").on('change',function(){
        query = {'test':$(this).val() };
        if( $("#m_id").val().length >= 2){
            query['m_id'] = $("#m_id").val();

            if( $("#s_id").val().length >= 2){
                query['s_id'] = $("#s_id").val();
            }
        }

        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/jg/ajax_testchange/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#qtable').children().remove();
            $('#qanswer').children().remove();

            for( var i = 0 ;  i < data.length ; i++){

                $td1 = $('<td>').text("【" + data[i]['q_id'] + "】 " + data[i]['q_title'] );
                $td1.attr("style","font-size:12pt;");
                $tr1 = $("<tr>").append( $td1 );

                $img = $("<img src='/static/jg/image/question/" + data[i]['q_id'] + ".png'>" );
                $img.attr("style","width:800px;");
                $img.attr("class","q_img");
                $td2 = $('<td>').append($img);
                $tr2 = $('<tr>').append($td2);

                $('#qtable').append( $tr1 );
                $('#qtable').append( $tr2 );

            }

            for( var i = 0 ; i < data.length ; i++ ){
                if( i == 0 ){
                    $div = $('<div>').attr('class','col');
                    $table = $('<table>').attr('class','table table-condensed').attr('style','width:80px');
                    $tr = $('<tr>');
                    $tr.append( $('<td>').text(data[i]['q_id']));
                    $tr.append( $('<td>').text( data[i]['q_answer']));
                    $table.append( $tr );
                    $div.append( $table );
                }else if( i % 20 == 0 ){
                    $('#qanswer').append( $div );
                    $div = $('<div>').attr('class','col');
                    $table = $('<table>').attr('class','table table-condensed').attr('style','width:80px');
                    $tr = $('<tr>');
                    $tr.append( $('<td>').text(data[i]['q_id']));
                    $tr.append( $('<td>').text( data[i]['q_answer']));
                    $table.append( $tr );
                    $div.append( $table );
                }else{
                    $tr = $('<tr>');
                    $tr.append( $('<td>').text(data[i]['q_id']));
                    $tr.append( $('<td>').text( data[i]['q_answer']));
                    $table.append( $tr );
                }
            }
            $('#qanswer').append( $div );
        }).fail( (data)=>{
            alert('fail');
        }).always( (data) => {

        });

    });

    //中分類変更
    $("#m_id").on('change',function(){
        query = {'test':$('#test').val() , 'm_id':$(this).val() };
        $('#s_id').val("");

        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/jg/ajax_m_id_change/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#qtable').children().remove();
            $('#qanswer').children().remove();
            list1 = data['list1'];
            list2 = data['list2']
            for( var i = 0 ;  i < list1.length ; i++){

                $td1 = $('<td>').text("【" + list1[i]['q_id'] + "】 " + list1[i]['q_title'] );
                $td1.attr("style","font-size:12pt;");
                $tr1 = $("<tr>").append( $td1 );

                $img = $("<img src='/static/jg/image/question/" + list1[i]['q_id'] + ".png'>" );
                $img.attr("style","width:800px;");
                $img.attr("class","q_img");
                $td2 = $('<td>').append($img);
                $tr2 = $('<tr>').append($td2);

                $('#qtable').append( $tr1 );
                $('#qtable').append( $tr2 );

            }

            for( var i = 0 ; i < list1.length ; i++ ){
                if( i == 0 ){
                    $div = $('<div>').attr('class','col');
                    $table = $('<table>').attr('class','table table-condensed').attr('style','width:80px');
                    $tr = $('<tr>');
                    $tr.append( $('<td>').text(list1[i]['q_id']));
                    $tr.append( $('<td>').text( list1[i]['q_answer']));
                    $table.append( $tr );
                    $div.append( $table );
                }else if( i % 20 == 0 ){
                    $('#qanswer').append( $div );
                    $div = $('<div>').attr('class','col');
                    $table = $('<table>').attr('class','table table-condensed').attr('style','width:80px');
                    $tr = $('<tr>');
                    $tr.append( $('<td>').text( list1[i]['q_id']));
                    $tr.append( $('<td>').text( list1[i]['q_answer']));
                    $table.append( $tr );
                    $div.append( $table );
                }else{
                    $tr = $('<tr>');
                    $tr.append( $('<td>').text( list1[i]['q_id']));
                    $tr.append( $('<td>').text( list1[i]['q_answer']));
                    $table.append( $tr );
                }
            }
            $('#qanswer').append( $div );

            //小分類
            $('#s_id').children().remove();
            $('#s_id').append( $('<option>'));
            for( var i = 0 ; i < list2.length ; i++ ){
                $('#s_id').append( $('<option>').val(list2[i]['s_id']).text(list2[i]['s_name']));
            }
        }).fail( (data)=>{
            alert('fail');
        }).always( (data) => {

        });

    });


    //小分類変更
   $("#s_id").on('change',function(){
        query = {'test':$('#test').val() , 's_id':$('#s_id').val(),'m_id':$('#m_id').val() };

        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/jg/ajax_s_id_change/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $('#qtable').children().remove();
            $('#qanswer').children().remove();

            for( var i = 0 ;  i < data.length ; i++){

                $td1 = $('<td>').text("【" + data[i]['q_id'] + "】 " + data[i]['q_title'] );
                $td1.attr("style","font-size:12pt;");
                $tr1 = $("<tr>").append( $td1 );

                $img = $("<img src='/static/jg/image/question/" + data[i]['q_id'] + ".png'>" );
                $img.attr("style","width:800px;");
                $img.attr("class","q_img");
                $td2 = $('<td>').append($img);
                $tr2 = $('<tr>').append($td2);

                $('#qtable').append( $tr1 );
                $('#qtable').append( $tr2 );

            }

            for( var i = 0 ; i < data.length ; i++ ){
                if( i == 0 ){
                    $div = $('<div>').attr('class','col');
                    $table = $('<table>').attr('class','table table-condensed').attr('style','width:80px');
                    $tr = $('<tr>');
                    $tr.append( $('<td>').text(data[i]['q_id']));
                    $tr.append( $('<td>').text( data[i]['q_answer']));
                    $table.append( $tr );
                    $div.append( $table );
                }else if( i % 20 == 0 ){
                    $('#qanswer').append( $div );
                    $div = $('<div>').attr('class','col');
                    $table = $('<table>').attr('class','table table-condensed').attr('style','width:80px');
                    $tr = $('<tr>');
                    $tr.append( $('<td>').text(data[i]['q_id']));
                    $tr.append( $('<td>').text( data[i]['q_answer']));
                    $table.append( $tr );
                    $div.append( $table );
                }else{
                    $tr = $('<tr>');
                    $tr.append( $('<td>').text(data[i]['q_id']));
                    $tr.append( $('<td>').text( data[i]['q_answer']));
                    $table.append( $tr );
                }
            }
            $('#qanswer').append( $div );
        }).fail( (data)=>{
            alert('fail');
        }).always( (data) => {

        });

    });


});