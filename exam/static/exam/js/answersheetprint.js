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

    $("#t_id").on('change',function(){
        query = {'t_id':$(this).val()};
        $.ajaxSetup({
            beforeSend : function(xhr,settings ){
                xhr.setRequestHeader( "X-CSRFToken" , getCSRFToken() );
            }
        });

        $.ajax({
            type:"POST",
            url:"/exam/answersheetprint_conf/",
            dataType:'json',
            contentType: 'charset=utf-8',
            data: getJsonStr( query ),
        }).done( (data) => {
            $print = $("#print");
            $print.children().remove();

            t_list = data['t_list'];
            u_list = data['u_list'];
            o_id = data['o_id'];

            //ユーザがいなくなるまで繰り返す
            for( var i = 0 ; i < u_list.length ; i = i + 1 ){

                $username = $("<p>").text( "ユーザ名:" + u_list[i]['u_name'] ).attr("class","user-name");

                $print.append( $username );

                $t_tr = $("<tr>").append(
                    $("<td>").append( $("<img>").attr("src","/static/exam/image/omr/marker.png") ).attr("class","marker"),
                    $("<td>").text( '組織ID').attr("colspan","5").attr("class","user"),
                    $("<td>").text( o_id ).attr("colspan","5").attr("class","num-id").attr("class","user"),
                    $("<td>").text( 'テストID' ).attr("colspan","5").attr("class","user"),
                    $("<td>").text( query['t_id']).attr("colspan","5").attr("class","num-id").attr("class","user"),
                );
                $u_tr = $("<tr>").append(
                    $("<td>").append( $("<img>").attr("src","/static/exam/image/omr/marker.png") ).attr("class","marker"),
                    $("<td>").text( 'ユーザID' ).attr("colspan","5").attr("class","user"),
                    $("<td>").text( u_list[i]['u_id'] ).attr("colspan","5").attr("class","num-id").attr("class","user"),
                    $("<td>").attr("colspan","5").attr("class","user"),
                    $("<td>").attr("colspan","5").attr("class","num-id").attr("class","user")
                );

                $table = $("<table>").attr("class","mark-sheet");
                
                $print.append( 
                    $("<div>").append( 
                        $table.append( $t_tr,$u_tr )
                    )
                );

                if( t_list.length == 10 | t_list.length == 20){
                    $table.append( 
                        $("<tr>").append(
                            $("<td>").append( $("<img>").attr("src","/static/exam/image/omr/marker.png") ).attr("class","marker"),
                            $("<th>").attr("class","t-head").text("No"),
                            $("<th>").attr("class","t-head").text("ア"),
                            $("<th>").attr("class","t-head").text("イ"),
                            $("<th>").attr("class","t-head").text("ウ"),
                            $("<th>").attr("class","t-head").text("エ")
                        )
                    );
                    for( var j = 0 ; j < 20 ; j = j + 1 ){
                        $table.append( 
                            $("<tr>").append(
                                $("<td>").append( $("<img>").attr("src","/static/exam/image/omr/marker.png") ).attr("class","marker"),
                                $("<td>").text(t_list[j]['t_num']).attr("class","t-num"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru")
                            )
                        );                       
                                        
                    }
                }else if( t_list.length == 40 ){
                    $table.append( 
                        $("<tr>").append(
                            $("<td>").append( $("<img>").attr("src","/static/exam/image/omr/marker.png") ).attr("class","marker"),
                            $("<th>").text("No").attr("class","t-num"),
                            $("<th>").attr("class","t-head").text("ア"),
                            $("<th>").attr("class","t-head").text("イ"),
                            $("<th>").attr("class","t-head").text("ウ"),
                            $("<th>").attr("class","t-head").text("エ"),
                            $("<th>").text("No").attr("class","t-num"),
                            $("<th>").attr("class","t-head").text("ア"),
                            $("<th>").attr("class","t-head").text("イ"),
                            $("<th>").attr("class","t-head").text("ウ"),
                            $("<th>").attr("class","t-head").text("エ"),
                        )
                    );
                    for( var j = 0 ; j < 20 ; j = j + 1 ){
                        $table.append( 
                            $("<tr>").append(
                                $("<td>").append( $("<img>").attr("src","/static/exam/image/omr/marker.png") ).attr("class","marker"),
                                $("<td>").text(t_list[j]['t-num']).attr("class","t-num"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text(t_list[j+20]['t-num']).attr("class","t-num"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru")
                            )
                        );                       
                                         
                    }                    
                }else if( t_list.length == 60 ){
                    $table.append( 
                        $("<tr>").attr("class","t-head").append(
                            $("<td>").append( $("<img>").attr("src","/static/exam/image/omr/marker.png") ).attr("class","marker"),
                            $("<th>").text("No").attr("class","t-num"),
                            $("<th>").attr("class","t-head").text("ア"),
                            $("<th>").attr("class","t-head").text("イ"),
                            $("<th>").attr("class","t-head").text("ウ"),
                            $("<th>").attr("class","t-head").text("エ"),
                            $("<th>").text("No").attr("class","t-num"),
                            $("<th>").attr("class","t-head").text("ア"),
                            $("<th>").attr("class","t-head").text("イ"),
                            $("<th>").attr("class","t-head").text("ウ"),
                            $("<th>").attr("class","t-head").text("エ"),
                            $("<th>").text("No").attr("class","t-num"),
                            $("<th>").attr("class","t-head").text("ア"),
                            $("<th>").attr("class","t-head").text("イ"),
                            $("<th>").attr("class","t-head").text("ウ"),
                            $("<th>").attr("class","t-head").text("エ"),
                        )
                    );
                    for( var j = 0 ; j < 20 ; j = j + 1 ){
                        $table.append( 
                            $("<tr>").append(
                                $("<td>").append( $("<img>").attr("src","/static/exam/image/omr/marker.png") ).attr("class","marker"),
                                $("<td>").text(t_list[j]['t-num']).attr("class","t-num"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text(t_list[j+20]['t-num']).attr("class","t-num"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text(t_list[j+40]['t-num']).attr("class","t-num"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                            )
                        );                       
                                      
                    }
                }else{
                    $table.append( 
                        $("<tr>").attr("class","t-head").append(
                            $("<td>").append( $("<img>").attr("src","/static/exam/image/omr/marker.png") ).attr("class","marker"),
                            $("<th>").text("No").attr("class","t-num"),
                            $("<th>").attr("class","t-head").text("ア"),
                            $("<th>").attr("class","t-head").text("イ"),
                            $("<th>").attr("class","t-head").text("ウ"),
                            $("<th>").attr("class","t-head").text("エ"),
                            $("<th>").text("No").attr("class","t-num"),
                            $("<th>").attr("class","t-head").text("ア"),
                            $("<th>").attr("class","t-head").text("イ"),
                            $("<th>").attr("class","t-head").text("ウ"),
                            $("<th>").attr("class","t-head").text("エ"),
                            $("<th>").text("No").attr("class","t-num"),
                            $("<th>").attr("class","t-head").text("ア"),
                            $("<th>").attr("class","t-head").text("イ"),
                            $("<th>").attr("class","t-head").text("ウ"),
                            $("<th>").attr("class","t-head").text("エ"),
                            $("<th>").text("No").attr("class","t-num"),
                            $("<th>").attr("class","t-head").text("ア"),
                            $("<th>").attr("class","t-head").text("イ"),
                            $("<th>").attr("class","t-head").text("ウ"),
                            $("<th>").attr("class","t-head").text("エ"),
                        )
                    );
                    for( var j = 0 ; j < 20 ; j = j + 1 ){
                        $table.append( 
                            $("<tr>").append(
                                $("<td>").append( $("<img>").attr("src","/static/exam/image/omr/marker.png") ).attr("class","marker"),
                                $("<td>").text(t_list[j]['t_num']).attr("class","t-num"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text(t_list[j+20]['t_num']).attr("class","t-num"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text(t_list[j+40]['t_num']).attr("class","t-num"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text(t_list[j+60]['t_num']).attr("class","t-num"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                                $("<td>").text("〇").attr("class","maru"),
                            )
                        );                                        
                    }

                }


                /*
                for( var j = 0 ; j < t_list.length ;  j = j + 1 ){
                    if( j == 0 | j == 20 | j == 40 | j == 60){

                        $table = $("<table>").attr("class","test").append( 
                            $("<tr>").append( 
                                $("<th>").text("No"), $("<th>").text("ア"),$("<th>").text("イ"),$("<th>").text("ウ"),$("<th>").text("エ")
                            )
                        );
                        
                        $row.append( 
                            $("<div>").attr("class","col").append($table)
                        );
                    }
                    $table.append( 
                        $("<tr>").append( 
                            $("<td>").text(t_list[j]['t_num']).attr("class","t_num"),
                            $("<td>").text("〇").attr("class","maru"),
                            $("<td>").text("〇").attr("class","maru"),
                            $("<td>").text("〇").attr("class","maru"),
                            $("<td>").text("〇").attr("class","maru")
                        )
                    );
                }
                
                if( t_list.length == 10 | t_list.length == 20 ){
                    $row.append( $("<div>").attr("class","col") );
                    $row.append( $("<div>").attr("class","col") );
                    $row.append( $("<div>").attr("class","col") );
                }else if( t_list.length == 40 ){
                    $row.append( $("<div>").attr("class","col") );
                    $row.append( $("<div>").attr("class","col") );                   
                }else if( t_list.length == 60 ){
                    $row.append( $("<div>").attr("class","col") ); 
                }*/


                $print.append(
                    $("<div>").attr("style","page-break-after: always")
                );
            }

            $('#modal-progress').modal('hide');

        }).fail( (data)=>{
            alert('fail');
        }).always( (data) => {

        });

    });


});