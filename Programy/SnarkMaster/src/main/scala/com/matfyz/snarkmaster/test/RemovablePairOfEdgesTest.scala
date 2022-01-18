package com.matfyz.snarkmaster.test

import com.matfyz.snarkmaster.common.task
import com.matfyz.snarkmaster.configuration.Configuration
import com.matfyz.snarkmaster.graph.Graph

case object StartRemovablePairOfEdgesTest extends StartTestMessage {
  override def start(graphs: Seq[Graph], configuration: Configuration) = {
    RemovablePairOfEdgesTest.test(graphs, configuration)
  }
}

object RemovablePairOfEdgesTest extends SnarkRemovabilityTest {
  override def test(graph: Graph, configuration: Configuration): SnarkTestResult = {

    val edges = graph.edges.toSeq

    val tests = {
      for {
        i <- edges.indices
        j <- (i+1) until edges.size
      } yield {
        val g = graph.removeEdge(edges(i)).removeEdge(edges(j))
        task ((edges(i),edges(j)), runTest(g, configuration))
      }
    }.map(_.join())

    RemovablePairOfEdgesTestResult(graph, configuration, tests.filter(_._2).map(_._1))
  }

  def runTest(graph: Graph, configuration: Configuration): Boolean  = {
    SATColoringTest.tryToColor(graph, configuration) match {
      case Some(model) => false
      case None => true
    }
  }
}
