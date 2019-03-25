<?php
   function getall(){
      $user;
      // echo "python3 /var/www/mthz/showcase/python/Users_Spider.py 2>&1 $_GET[mid] 0";
      $userinfo = exec("python3 /var/www/mthz/showcase/python/Users_Spider.py 2>&1 $_GET[mid] $_GET[action] $_GET[pg]",$user);
      // 2>&1将标准错误重定向到标准输出
      // echo $user;
      for($x=0;$x<count($user);$x++)
      {
         echo $user[$x];
      }
      return $user;
   }
   getall();
?>