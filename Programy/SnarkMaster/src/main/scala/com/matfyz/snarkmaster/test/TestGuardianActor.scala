package com.matfyz.snarkmaster.test

import akka.actor.{Actor, ActorRef}
import akka.event.LoggingReceive
import com.matfyz.snarkmaster.model.{LogText, TestComponents, TestGraphs}

import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.{ExecutionContext, Future}

class TestGuardianActor(listener: ActorRef) extends Actor{
  override def receive: Receive = LoggingReceive{
    case TestGraphs(graphs, configuration, tests) =>
      val originSender = sender
      Future{
        tests.foreach{ test =>
          listener ! LogText("Start test graphs: " + graphs.map(_.name).mkString(", "))
          val testResult = test.start(graphs, configuration)
          originSender ! testResult
        }
      }
    case TestComponents(component, configuration, tests) =>
      val originSender = sender
      Future{
        tests.foreach{ test =>
          listener ! LogText("Start test component: " + component.head.graph.name)
          val testResult = test.start(component, configuration)
          originSender ! testResult
        }
      }
  }
}

object TestGuardianActor{
  val actorName = "test-guardian"
}
