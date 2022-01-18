package com.matfyz.snarkmaster.parser.format

import java.io.File

import com.matfyz.snarkmaster.graph.Graph

object TripleGraphFormat extends GraphFileFormat{
  override def parse(file: File, lines: Iterator[String]): Seq[Graph] = {
    val in = lines.filter(!_.startsWith("{"))
      .flatMap(_.split(" ").map(_.toInt))

    val numberOfGraphs = in.next()

    for(graphNumber <- 0 until numberOfGraphs) yield {
      in.next() // graph number
      val numberOfVertices = in.next

      in.take(numberOfVertices * 3)
        .sliding(3, 3)
        .zipWithIndex
        .flatMap{ case (n, v) => n.map((v, _))}
        .foldLeft(new Graph(file.getName + "(" + (graphNumber+1) + ")")){case (g, (u, v)) =>
          g.addVertex(u)
            .addVertex(v)
            .addBidirectionalEdge(u, v, false)
        }
    }
  }
}
