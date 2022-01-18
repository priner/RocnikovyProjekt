package com.matfyz.snarkmaster

import akka.actor.{Actor, Props}
import akka.event.LoggingReceive
import com.matfyz.snarkmaster.model._
import com.matfyz.snarkmaster.parser.GraphParserActor
import com.matfyz.snarkmaster.test.TestGuardianActor
import com.matfyz.snarkmaster.ui.UIGuardianActor

class NodeGuardian() extends Actor{
  val uiActor = context.actorOf(Props(new UIGuardianActor(self)), UIGuardianActor.actorName)
  val testGuardianActor =  context.actorOf(Props(new TestGuardianActor(self)), TestGuardianActor.actorName)
  val graphParserActor = context.actorOf(Props(new GraphParserActor(self)), GraphParserActor.actorName)

  override def receive: Receive = LoggingReceive {
    case m: LogMessage => uiActor forward m
    case m: ParseGraph => graphParserActor forward m
    case m: ParseComponent => graphParserActor forward m
    case m: TestGraphs => testGuardianActor forward m
    case m: TestComponents => testGuardianActor forward m
    case _ =>
  }

  uiActor ! LogText("SnarkMaster started!")

}

object NodeGuardian {

  val name = "node-guardian"

}
