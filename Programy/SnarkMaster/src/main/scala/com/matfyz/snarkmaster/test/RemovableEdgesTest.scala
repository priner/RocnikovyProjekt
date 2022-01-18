package com.matfyz.snarkmaster.test

import com.matfyz.snarkmaster.common.task
import com.matfyz.snarkmaster.configuration.Configuration
import com.matfyz.snarkmaster.graph.Graph

case object StartRemovableEdgesTest extends StartTestMessage {
  override def start(graphs: Seq[Graph], configuration: Configuration) = {
    RemovableEdgesTest.test(graphs, configuration)
  }
}

object RemovableEdgesTest extends SnarkRemovabilityTest {
  override def test(graph: Graph, configuration: Configuration): SnarkTestResult = {

    val tests = graph.edges.map { e =>
      task{
        (e, runTest(graph.removeEdge(e), configuration))
      }
    }.map(_.join())

    RemovableEdgesTestResult(graph, configuration, tests.filter(_._2).map(_._1).toSeq)
  }

  def runTest(graph: Graph, configuration: Configuration): Boolean  = {
    SATColoringTest.tryToColor(graph, configuration) match {
      case Some(model) => false
      case None => true
    }
  }
}
