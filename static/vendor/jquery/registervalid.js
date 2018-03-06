  $(function() {
        $("#id_username").blur(
            function(){
                var username = $("#id_username").val();
                if (username){}
                else{
                    $("#error_3").text("用户名不可为空");
                    $("#submitButton").attr("disabled", true)
                }
            }
        );

        $("#id_phone").blur(
                function(){
                    var phone = $("#id_phone").val();
                    if (phone) {
                        $.ajax(
                                {
                                    url: "/user/registervalid/",
                                    type: "POST",
                                    data: {"phone":phone},
                                    success:function(data){
                                        var Data = data.data;
                                        var statue = data.statue;
                                        console.log(Data);
                                        console.log(statue);
                                        if(statue == "error"){
                                            $("#error_3").text(Data);
                                            $("#submitButton").attr("disabled", true)
                                        }else{
                                            $("#error_3").text("");
                                            $("#submitButton").attr("disabled",false)
                                        }
                                    },
                                    error:function(error){
                                        console.log(error)
                                    }
                                }
                            )
                        }
                    else{
                         $("#error_3").text("手机号不可为空");
                         $("#submitButton").attr("disabled", true)
                    }
                }
        );

      $("#id_password").blur(
          function(){
                    var password = $("#id_password").val();
                    if (password) {
                        $.ajax(
                                {
                                    url: "/user/registervalid/",
                                    type: "POST",
                                    data: {"password":password},
                                    success:function(data){
                                        var Data = data.data;
                                        var statue = data.statue;
                                        console.log(Data);
                                        console.log(statue);
                                        if(statue == "error"){
                                            $("#error_3").text(Data);
                                            $("#submitButton").attr("disabled",true)
                                        }else{
                                            $("#error_3").text("");
                                            $("#submitButton").attr("disabled",false)
                                        }
                                    },
                                    error:function(error){
                                        console.log(error)
                                    }
                                }
                            )
                        }
                    else{
                         $("#error_3").text("密码不可为空");
                         $("#submitButton").attr("disabled", true)
                    }
                }
        );

      $("#id_email").blur(
          function(){
                    var email = $("#id_email").val();
                    if (email) {
                        $.ajax(
                                {
                                    url: "/user/registervalid/",
                                    type: "POST",
                                    data: {"email":email},
                                    success:function(data){
                                        var Data = data.data;
                                        var statue = data.statue;
                                        console.log(Data);
                                        console.log(statue);
                                        if(statue == "error"){
                                            $("#error_3").text(Data);
                                            $("#submitButton").attr("disabled",true)
                                        }else{
                                            $("#error_3").text("");
                                            $("#submitButton").attr("disabled",false)
                                        }
                                    },
                                    error:function(error){
                                        console.log(error)
                                    }
                                }
                            )
                        }
                    else{
                         $("#error_3").text("邮箱不可为空");
                         $("#submitButton").attr("disabled", true)
                    }
                }
        );
      });