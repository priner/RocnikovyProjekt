package com.matfyz.snarkmaster.graph

case class Edge(vertices: Set[Vertex])

object Edge{
  def apply(u: Vertex, v: Vertex): Edge = Edge(Set(u, v))
}
