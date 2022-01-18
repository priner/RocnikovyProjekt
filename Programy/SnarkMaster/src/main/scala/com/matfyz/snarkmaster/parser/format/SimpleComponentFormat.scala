package com.matfyz.snarkmaster.parser.format

import java.io.File

import com.matfyz.snarkmaster.graph.{Component, Graph}

object SimpleComponentFormat extends ComponentFileFormat{
  override def parse(file: File, lines: Iterator[String]): Seq[Component] = {
    val in = lines.filter(!_.startsWith("{"))
      .map(_.split(" ").map(_.toInt))

    val numberOfComponents = in.next.head

    for ( i <- 0 until numberOfComponents ) yield {
      // read graph number
      val graphIndex = in.next.head

      val numberOfVertices = in.next.head

      val graph =
        in.take(numberOfVertices).toList.zipWithIndex.flatMap { case (neigh, v) => neigh.map((_, v)) }
          .foldLeft(new Graph(file.getName + "(" + (i+1) + ")")) { case (g, (x, y)) =>
            g.addVertex(x)
              .addVertex(y)
              .addBidirectionalEdge(x, y)
          }


      val numberOfConnectors = in.next().head

      val connectors = in.take(numberOfConnectors).toList.map(x => (x(0), x(1)))

      Component(graph, connectors)
    }
  }
}
