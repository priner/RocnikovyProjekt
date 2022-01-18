package com.matfyz.snarkmaster.test

import com.matfyz.snarkmaster.configuration.Configuration
import com.matfyz.snarkmaster.graph.Graph
import org.scalatest.FlatSpec

class SATColoringTestSpec extends FlatSpec{
  behavior of "coloring test"

  it should "find coloring for K4" in {
    val graph = Graph(0->1, 0->2, 0->3, 1->2, 1->3, 2->3)

    val res = SATColoringTest.test(graph, Configuration.threeColoring)

    assert( res match {
      case ColoringExists(colors, _) =>
        val col = colors.map{case (a,b, f) => (a, b) -> f}.toMap
        col((0,1)) == col((2, 3)) && col((0, 3)) == col((1, 2)) && col((0,2)) == col((1, 3)) &&
          col((0,1)) != col((0, 2)) && col((0,1)) != col(0, 3)
      case _ => false
    })
  }

  it should "find out that petersen doesn't have 3 coloring" in {
    val graph = Graph(0->1,1->2,2->3,3->4,4->0,5->6,6->7,7->8,8->9,9->5,0->7,1->5,2->8,3->6,4->9)

    val res = SATColoringTest.test(graph, Configuration.threeColoring)

    assert(res.isInstanceOf[WithoutColoring])
  }
}
