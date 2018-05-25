//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);

    $.get('/order/showorders/',function(data){
        if(data.code == 200){
            // alert("200 /order/showorders/");
            var orders_list_tmp = template("orders-list-tmp",{orders:data.orders});
            $(".orders-list").append(orders_list_tmp);
            $(".order-comment").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-comment").attr("order-id", orderId);
            });
        }
    });

    $('.modal-comment').on('click',function () {
        var orderId = $(this).attr("order-id");
        var comment = $('#comment').val();
        $.ajax({
            url:'/order/comment/',
            type:'PUT',
            dataType:'json',
            data:{'order_id':orderId,'comment':comment},
            success:function (data) {
                if(data.code==200) {
                    location.href = "/order/order/"
                }
            },
            error:function (data) {
                alert("/order/comment/ error");
            }
        });
    });

});
