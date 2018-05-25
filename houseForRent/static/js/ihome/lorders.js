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

    // $(".order-accept").on("click", function(){
    //     // var orderId = $(this).parents("li").attr("order-id");
    //     var orderId = $("#temp2").val();
    //     // $(".modal-accept").attr("order-id", orderId);
    // });

    // $(".modal-accept").on("click",function () {
    //     var status = 0;
    //     // var order_id = $(this).attr('order-id');
    //     var order_id = $('#temp2').val();
    //     alert(status);
    //     alert(order_id);
    //     $.ajax({
    //         url: "/order/change_status/",
    //         type:"PUT",
    //         dataType:"json",
    //         data:{"status":status,"order_id":order_id},
    //         success:function (data) {
    //             if(data.code==200) {
    //                 alert("200");
    //                 $('#order_status').html(data.status);
    //                 $('.order-accept').hide();
    //                 $('.order-reject').hide();
    //             }
    //         },
    //         error:function(data) {
    //             alert(".modal-accept fail")
    //         }
    //     })
    // });

    // $(".order-reject").on("click", function(){
    //     var orderId = $(this).parents("li").attr("order-id");
    //     $(".modal-reject").attr("order-id", orderId);
    // });

    // $(".modal-reject").on("click", function(){
    //     var status = 1;
    //     var order_id = $(this).attr('order-id');
    //     alert(status);
    //     alert(order_id);
    //     $.ajax({
    //         url: "/order/change_status/",
    //         type:"PUT",
    //         dataType:"json",
    //         data:{"status":status,"order_id":order_id},
    //         success:function (data) {
    //             if(data.code==200) {
    //                 $('#order_status').html(data.status);
    //                 $('.order-accept').hide();
    //                 $('.order-reject').hide();
    //             }
    //         },
    //         error:function(data) {
    //             alert(".modal-reject fail")
    //         }
    //     });
    // });

    $.get('/order/customer_lorders/',function (data) {
        // 页面被重新渲染，点击事件需要重写，否则不生效
        if(data.code==200){
            // alert("/order/customer_lorders/");
            var customer_order_list = template('customer-order-list',{orders:data.orders});
            $('.orders-list').append(customer_order_list);

            $(".order-accept").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-accept").attr("order-id", orderId);
            });

            $(".order-reject").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-reject").attr("order-id", orderId);
            });

            $(".modal-accept").on("click",function () {
                var status = 0;
                var order_id = $(this).attr('order-id');
                // alert(status);
                // alert(order_id);
                $.ajax({
                    url: "/order/change_status/",
                    type:"PATCH",
                    dataType:"json",
                    data:{"status":status,"order_id":order_id},
                    success:function (data) {
                        if (data.code == 200) {
                            // alert("200");
                            // $('#order_status').html(data.status);
                            // $('.order-accept').hide();
                            // $('.order-reject').hide();
                            // $('#order_id_' + order_id).html("待支付");
                            // $('.order-operate').hide();
                            // $('.modal-dialog').hide();
                            //$('#accept-modal').modal('hide'); //整个模块动态隐藏,下一次点击后照常显示
                            location.href = "/order/lorders/"

                        }
                    },
                    error:function(data) {
                        alert(".modal-accept fail")
                    }
                })
            });

            $(".modal-reject").on("click", function(){
                var status = 1;
                var order_id = $(this).attr('order-id');
                var comment = $('#reject-reason').val();
                // alert(status);
                // alert(order_id);
                $.ajax({
                    url: "/order/change_status/",
                    type:"PATCH",
                    dataType:"json",
                    data:{"status":status,"order_id":order_id,"comment":comment},
                    success:function (data) {
                        if(data.code==200) {
                            // $('#order_status').html(data.status);
                            // $('.order-accept').hide();
                            // $('.order-reject').hide();

                            // $('#order_id_' + order_id).html(data.status);
                            // $('.order-operate').hide();
                            // $('.modal-dialog').hide();
                            // $('#accept-modal').hide();
                            // $('.modal-backdrop').css({'display':'None'})
                            //$('#reject-modal').modal('hide'); //整个模块动态隐藏,下一次点击后照常显示
                             location.href = "/order/lorders/"
                        }
                    },
                    error:function(data) {
                        alert(".modal-reject fail")
                     }
                });
            });

        }
    });
});