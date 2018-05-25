function logout() {
    // $.get("/user/logout", function(data){
    //     if (data.code==200) {
    //         location.href = "/user/login/";
    //     }
    // })
    $.ajax({
       url:'/user/logout/',
       type:'DELETE',
       dataType:'json',
       success:function (data) {
          if(data.code==200){
              // alert("my logout");
              location.href = "/user/login/"
          }
       },
       error:function (data) {
           alert("my logout fail!")
       }
    });

}

$(document).ready(function(){
    $.get('/user/user',function (data) {
        if(data.code == '200'){
            $('#user-mobile').html(data.user.phone);
            $('#user-name').html(data.user.name);
            $('#user-avatar').attr('src',data.user.avatar);
        }
    })
});