package com.matfyz.snarkmaster.parser.format

import java.io.File

import com.matfyz.snarkmaster.graph.Graph
import org.scalatest.FlatSpec

class SimpleTripleFormatSpec extends FlatSpec{
  import SimpleTripleFormatSpec._

  behavior of "parse"

  it should "parse simple graph" in {
    val res = TripleGraphFormat.parse(new File(""), rawData1.split("\n").toIterator)
    assert(res === graphs1)
  }
}

object SimpleTripleFormatSpec{
  val rawData1 =
    """1
      |{comment}
      |1
      |4
      |1 2 3
      |2 3 0
      |0 3 1
      |0 2 1
    """.stripMargin

  val graphs1 = Seq(Graph.apply(
    (0, 1), (0, 2), (0, 3),
    (1, 2), (1, 3),
    (2, 3)
  ))
}