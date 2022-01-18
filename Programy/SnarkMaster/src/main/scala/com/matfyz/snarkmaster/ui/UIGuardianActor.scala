package com.matfyz.snarkmaster.ui

import akka.actor.{Actor, ActorRef, Props}
import com.matfyz.snarkmaster.model._

class UIGuardianActor(listener: ActorRef) extends Actor{

  val mainFrame = new MainForm()
  mainFrame.run()

  val logActor = context.actorOf(Props(new LogActor(self, mainFrame)), LogActor.actorName)
  val coloringTabActor = context.actorOf(Props(new ColoringTabActor(self, mainFrame)), ColoringTabActor.actorName)
  val transitionsTabActor = context.actorOf(Props(new TransitionsTabActor(self, mainFrame)), TransitionsTabActor.actorName)
  val removabilityTabActor = context.actorOf(Props(new RemovabilityTabActor(self, mainFrame)), RemovabilityTabActor.actorName)

  override def receive: Receive = {
    case m: LogMessage => logActor forward m
    case m: ParseGraph => listener forward m
    case m: ParseComponent => listener forward m
    case m: TestGraphs => listener forward m
    case m: TestComponents => listener forward m
  }
}

object UIGuardianActor{
  val actorName = "ui-actor"
}