package com.matfyz.snarkmaster.test

import com.matfyz.snarkmaster.common.task
import com.matfyz.snarkmaster.configuration.Configuration
import com.matfyz.snarkmaster.graph.Graph

case object StartRemovableVerticesTest extends StartTestMessage {
  override def start(graphs: Seq[Graph], configuration: Configuration) = {
    RemovableVerticesTest.test(graphs, configuration)
  }
}

object RemovableVerticesTest extends SnarkRemovabilityTest{
  override def test(graph: Graph, configuration: Configuration): SnarkTestResult = {

    val tests = graph.vertices.keys.map { v =>
      task{
        (v, runTest(graph.removeVertex(v), configuration))
      }
    }.map(_.join())

    RemovableVerticesTestResult(graph, configuration, tests.filter(_._2).map(_._1).toSeq.sorted)
  }

  def runTest(graph: Graph, configuration: Configuration): Boolean  = {
    SATColoringTest.tryToColor(graph, configuration) match {
      case Some(model) => false
      case None => true
    }
  }
}
