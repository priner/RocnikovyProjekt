package com.matfyz.snarkmaster.parser.format
import java.io.File

import com.matfyz.snarkmaster.graph.Graph

object SimpleGraphFormat extends GraphFileFormat{
  override def parse(file: File, lines: Iterator[String]): Seq[Graph] = {
    val in = lines.filter(!_.startsWith("{"))
      .map(_.split(" ").map(_.toInt))

    val numberOfVertices = in.next.head

    Seq(
      in.take(numberOfVertices).zipWithIndex.flatMap{ case(neigh, v) => neigh.map((_, v))}
        .foldLeft(new Graph(file.getName)){ case(g, (x,y)) =>
          g.addVertex(x)
            .addVertex(y)
            .addBidirectionalEdge(x, y)
        }
    )
  }
}
