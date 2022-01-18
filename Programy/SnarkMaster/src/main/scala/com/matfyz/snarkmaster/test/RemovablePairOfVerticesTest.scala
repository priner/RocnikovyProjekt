package com.matfyz.snarkmaster.test

import com.matfyz.snarkmaster.common.task
import com.matfyz.snarkmaster.configuration.Configuration
import com.matfyz.snarkmaster.graph.Graph

case object StartRemovablePairOfVerticesTest extends StartTestMessage {
  override def start(graphs: Seq[Graph], configuration: Configuration) = {
    RemovablePairOfVerticesTest.test(graphs, configuration)
  }
}

object RemovablePairOfVerticesTest extends SnarkRemovabilityTest{
  override def test(graph: Graph, configuration: Configuration): SnarkTestResult = {

    val vertexIndices = graph.vertices.keys.toSeq.sorted

    val tests = {
      for {
        i <- vertexIndices.indices
        j <- (i + 1) until vertexIndices.size
      } yield {
        val x = vertexIndices(i)
        val y = vertexIndices(j)
        val g1 = graph.removeVertex(x)
        val g = if(y > x) g1.removeVertex(y-1) else g1.removeVertex(y)
        task ((vertexIndices(i), vertexIndices(j)), runTest(g, configuration))
      }
    }.map(_.join())

    RemovablePairOfVerticesTestResult(graph, configuration, tests.filter(_._2).map(_._1).sorted)
  }

  def runTest(graph: Graph, configuration: Configuration): Boolean  = {
    SATColoringTest.tryToColor(graph, configuration) match {
      case Some(model) => false
      case None => true
    }
  }
}
