package com.matfyz.snarkmaster.ui

import java.text.SimpleDateFormat
import java.util.Date

import akka.actor.{Actor, ActorRef}
import com.matfyz.snarkmaster.model.{LogException, LogResult, LogText}
import com.matfyz.snarkmaster.test._

class LogActor(listener: ActorRef, mainFrame: MainForm) extends Actor {
  import LogActor._

  val textArea = mainFrame.logTextArea

  override def receive: Receive = {
    case LogText(msg) =>
      textArea.append(logFormat(msg))
    case LogResult(results) =>
      results.foreach(r => textArea.append(logFormat(logResult(r))))
    case LogException(msg, ex) =>
      textArea.append(logFormat(msg))
      ex.foreach(t => textArea.append(logFormat(t.toString)))
  }

}

object LogActor{
  val actorName = "log-panel"

  private def logResult(result: SnarkTestResult): String = {
    result match {
      case WithoutColoring(graph) => "Graph " + graph.name + " hasn't coloring!"

      case ColoringExists(coloring, graph) =>
        "Graph " + graph.name + " has coloring \n" +
          coloring.sorted.map{ x => f"(${x._1}%3d, ${x._2}%3d) -> ${x._3}%3d"}.mkString("\t","\n\t","")

      case r: TransitionResult => "Graph " + r.graph.name + " has " + r.transitions.size + " transitions\n" +
        "edge vertices are " + r.edgeVertices.mkString("(", ", ", ")") + "\n" +
          r.rawTransitions.map(x=> x.map(_.id).mkString(", ")).sorted.mkString("\t","\n\t","\n") +
          "edge vertices are " + r.edgeVertices.mkString("(", ", ", ")") + "\n" +
          r.transitions.map(x=> x.mkString(", ")).toSeq.sorted.mkString("\t","\n\t","\n")

      case TransitionExists(graph, _) =>
        "Graph " + graph.name + " has some transition"

      case TransitionDoesntExists(graph, _) =>
        "Graph " + graph.name + " has no transition"

      case RemovableVerticesTestResult(graph, _, vertices) =>
        s"Graph ${graph.name} has ${vertices.size} removable vertices: ${vertices.mkString(", ")}"

      case RemovablePairOfVerticesTestResult(graph, _, pairs) =>
        s"Graph ${graph.name} has ${pairs.size} removable pairs of vertices: ${pairs.mkString(", ")}"

      case RemovableEdgesTestResult(graph, _, edges) =>
        val intEdges = edges.map(_.vertices.map(_.id).toSeq.sorted)
          .map(x => (x(0), x(1)))
          .sorted
        s"Graph ${graph.name} has ${edges.size} removable edges: ${intEdges.mkString(", ")}"

      case RemovablePairOfEdgesTestResult(graph, _, edges) =>
        val intEdges = edges.map{case (e,f) => (e.vertices.map(_.id).toSeq.sorted , f.vertices.map(_.id).toSeq.sorted)}
          .map{case (e,f) => s"[(${e(0)}, ${e(1)}), (${f(0)},${f(1)})]"}
          .sorted
        s"Graph ${graph.name} has ${edges.size} removable pairs of edges: ${intEdges.mkString(", ")}"
    }
  }

  val dateFormater = new SimpleDateFormat("dd-MM-yyyy  HH:mm:ss,SSS")

  private def logFormat(msg: String) = {
    dateFormater.format(new Date()) + " :  " + msg + "\n"
  }
}