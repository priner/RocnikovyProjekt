package com.matfyz.snarkmaster

import akka.actor.{ActorSystem, Props}

object SnarkMasterApp extends App{
 val system = ActorSystem("SnarkMaster")

 val nodeGuardian = system.actorOf(Props(new NodeGuardian()), NodeGuardian.name)

}
