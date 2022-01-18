package com.matfyz.snarkmaster.parser

import java.io.File

import akka.actor.{Actor, ActorRef}
import akka.event.LoggingReceive
import com.matfyz.snarkmaster.parser.format.{GraphFileFormat, SimpleGraphFormat, TripleGraphFormat}
import com.matfyz.snarkmaster.model._

class GraphParserActor(listener: ActorRef) extends Actor{
  override def receive: Receive = LoggingReceive {
    case ParseGraph(file, format) =>
      listener ! LogText("Start parsing file: " + file.getName)
      try {
        sender ! ParsedGraphs(format.parse(file), file)
      } catch {
        case ex: Exception =>
          listener ! LogException("Parsing error!", Some(ex))
      }
    case ParseComponent(file, format) =>
      listener ! LogText("Start parsing file: " + file.getName)
      try {
        sender ! ParsedComponents(format.parse(file), file)
      } catch {
        case ex: Exception =>
          listener ! LogException("Parsing error!", Some(ex))
      }
  }
}

object GraphParserActor{
  val actorName = "graph-parser"
}