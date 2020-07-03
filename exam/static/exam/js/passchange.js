$(function(){

    $('#p_form').submit('click',function(){
        $old_pass = $('#old_pass');
        $pass1 = $('#new_pass1');
        $pass2 = $('#new_pass2');

        if( $old_pass.val().length <= 0 || $pass1.val().length <= 0 || $pass2.val().length <= 0 ){
            alert('すべて入力が必要です。');
            return false;
        }

        if( $old_pass.val() == $pass1.val() ){
            alert('古いパスワードと新しいパスワードは違うものにしてください。');
            return false;
        }

        if( $pass1.val() == $pass2.val() ){

            return true;

        }else{
            alert('新しいパスワードが一致しません。');
            return false;
        }
    });

});