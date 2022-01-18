package com.matfyz.snarkmaster.test

import com.matfyz.snarkmaster.configuration.Configuration
import com.matfyz.snarkmaster.graph.Graph
import com.matfyz.snarkmaster.solver.LingelingSolver
import sat.formulas._

case object StartSatColoringTest extends StartTestMessage {
  override def start(graphs: Seq[Graph], configuration: Configuration) = {
    SATColoringTest.test(graphs, configuration)
  }
}

object SATColoringTest extends SnarkColoringTest{
  def test(graph: Graph, configuration: Configuration) = {
    try {
      tryToColor(graph, configuration) match {
        case Some(model) =>
          ColoringExists(
            model.map{ v =>
              val row = v.name.split(" ")
              val u1 = row(1).toInt
              val u2 = row(2).toInt
              val c = row(4).split("_").head.toInt
              (Math.min(u1, u2), Math.max(u1, u2), c)
            }.toSeq,
            graph
          )
        case None => WithoutColoring(graph)
      }
    } catch {
      case e: Throwable => println(e.getMessage)
        e.printStackTrace()
        WithoutColoring(graph)
    }
  }

  def tryToColor(graph: Graph, configuration: Configuration): Option[Set[Var]] = {
    val vertices = graph.getSize
    val colors = configuration.colors

    // matrix vertex x vertex x color
    val edgeVars = (0 until vertices).map(i => (0 until vertices).map { j =>
      if (graph.areNeighbour(i, j)) (0 until colors.size).map(c => Var(s"edge $i $j -> $c"))
      else Nil
    })

    val allConditions = CNF(
      additionalConditions(edgeVars, graph, configuration).clauses ++
        symmetry(edgeVars).clauses ++
        onePerEdge(edgeVars).clauses ++
        uniquePerEdge(edgeVars).clauses ++
        blocksConditions(edgeVars, configuration).clauses
    )

    val solver = new LingelingSolver()

    val solved = solver.solve(edgeVars.flatMap(_.flatten).toSet, allConditions)

    solved
  }

  def additionalConditions(edgeVars: Seq[Seq[Seq[Var]]], graph: Graph, configuration: Configuration): CNF = {
    if(configuration == Configuration.THConfiguration){
      val edge = graph.edges.head.vertices.toSeq.map(_.id)
      CNF(Set(Set(edgeVars(edge(0))(edge(1))(0), edgeVars(edge(0))(edge(1))(1)),
        Set(edgeVars(edge(1))(edge(0))(0), edgeVars(edge(1))(edge(0))(1))))
    } else CNF(Set())
  }

  def symmetry(vars: Seq[Seq[Seq[Var]]]): CNF = {
    CNF( {for{
      i <- vars.indices
      j <- vars(i).indices
      k <- vars(i)(j).indices
      if i < j
      c <- CNF.convert(vars(i)(j)(k) <-> vars(j)(i)(k)).clauses
    } yield c}.toSet )
  }

  def onePerEdge(vars: Seq[Seq[Seq[Var]]]): CNF = {
    CNF(vars.flatMap(_.filter(_.nonEmpty).map(_.toSet[Formula])).toSet)
  }

  def uniquePerEdge(vars: Seq[Seq[Seq[Var]]]): CNF = {
    CNF(vars.flatMap(_.flatMap{ p =>
      for{ i <- p
           j <- p
           if i != j
      } yield Set[Formula](Not(i), Not(j))
    }.toSet).toSet)
  }

  def blocksConditions(edgeVars: Seq[Seq[Seq[Var]]],
                       configuration: Configuration): CNF = {
    val fromOne = edgeVars.flatMap { row =>
      val n = row.zipWithIndex.filter(_._1.nonEmpty).map(_._2)
      val colsForNeigh = configuration.colors.map{ c =>
        c.id -> {for{
          b <- configuration.blocks
          if b.points.contains(c)
          p <- b.points
          if p != c
        } yield p.id}
      }.toMap

      for{
        i <- n
        j <- n
        if i != j
        c <- configuration.colors.map(_.id)
      } yield {
        row(i)(c) -> or( colsForNeigh(c).map(x => row(j)(x)).toSeq:_* )
      }

    }

    val fromTwo = edgeVars.flatMap { row =>
      val n = row.zipWithIndex.filter(_._1.nonEmpty).map(_._2)
      val colsForNeigh = configuration.blocks.flatMap{ b =>
        b.points.toSeq.permutations.map(p => (p(0).id,p(1).id) -> p(2).id)
      }.toMap

      for{
        i <- n
        j <- n
        if i != j
        k <- n
        if i != k && j != k
        c <- colsForNeigh
      } yield {
        (row(i)(c._1._1) && row(j)(c._1._2)) -> row(k)(c._2)
      }

    }

    CNF((fromOne ++ fromTwo).flatMap(x => CNF.convert(x).clauses).toSet)
  }
}
