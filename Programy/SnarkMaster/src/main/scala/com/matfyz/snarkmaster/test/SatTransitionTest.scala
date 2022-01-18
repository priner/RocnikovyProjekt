package com.matfyz.snarkmaster.test
import com.matfyz.snarkmaster.common._
import com.matfyz.snarkmaster.configuration.{Configuration, Point}
import com.matfyz.snarkmaster.graph.Component
import com.matfyz.snarkmaster.solver.LingelingSolver
import sat.formulas.CNF
import sat.formulas._

case object StartTransitionTest extends StartComponentTestMessage{
  override def start(components: Seq[Component], configuration: Configuration): Seq[SnarkTestResult] = {
    components.flatMap(component => SATTransitionTest.findTransition(component, configuration))
  }
}

object SATTransitionTest {
  def findTransition(component: Component, configuration: Configuration): Seq[SnarkTestResult] = {
    try {
      val graph = component.graph
      val vertices = graph.getSize
      val colors = configuration.colors

      val normalVerices = graph.vertices.filter(x => graph.getNeighbour(x._1).size == 3).keys.toSeq.sorted
      val connectorVerices = component.connectors.flatMap(t => Seq(t._1, t._2))
      val residual = (graph.vertices.keys.toSet -- normalVerices) -- connectorVerices
      val edgeVerices = connectorVerices ++ residual.toSeq

      //println(edgeVerices)

      val combinations = {
        for {i <- colors.toSeq
             j <- edgeVerices}
          yield i
      }.combinations(edgeVerices.size)
        .flatMap(_.permutations)
        .toSeq
        .filter(tHTransitionFilter)

      // matrix vertex x vertex x color
      val edgeVars = (0 until vertices).map(i => (0 until vertices).map { j =>
        if (graph.areNeighbour(i, j)) (0 until colors.size).map(c => Var(s"edge $i $j -> $c"))
        else Nil
      })

      val baseConditions = CNF(
        SATColoringTest.symmetry(edgeVars).clauses ++
          SATColoringTest.onePerEdge(edgeVars).clauses ++
          SATColoringTest.uniquePerEdge(edgeVars).clauses ++
          SATColoringTest.blocksConditions(edgeVars, configuration).clauses
      )

      val result = new Array[Boolean](combinations.size)

      val jobs = combinations.indices.map { i =>
        task {
          val r = tryToColor(combinations(i), edgeVerices, baseConditions, edgeVars)
          result.update(i, r)
          //println(combinations(i) + " res = " + r)
        }
      }.foreach(_.join())

      val goodColorings = combinations.zip(result).filter(_._2).map(_._1)
      //println("good: \n" + goodColorings.mkString("\n"))

      val resTrans = goodColorings.map { col =>
        col.take(component.connectors.size * 2).sliding(2, 2).map(t => Configuration.mapToFactor((t(0), t(1)))).toSeq
      }.toSet


      Seq(TransitionResult(graph, configuration, resTrans, goodColorings, edgeVerices))
    } catch {
      case e: Throwable =>
        e.printStackTrace()
        Nil
    }
  }

  def tryToColor(colors: Seq[Point], vertices: Seq[Int], conditions: CNF, vars: Seq[Seq[Seq[Var]]]): Boolean = {
    val transitionConditions = setTransitionEdges(colors, vertices, vars).map(CNF.convert)
    val allConditions = CNF(conditions.clauses ++ transitionConditions.flatMap(_.clauses))
    new LingelingSolver().solve(vars.flatMap(_.flatten).toSet, allConditions) match {
      case None => false
      case Some(model) => true
    }
  }

  def setTransitionEdges(colors: Seq[Point], vertices: Seq[Int], vars: Seq[Seq[Seq[Var]]]) = {
    colors.zip(vertices).map { case (c, v) =>
      val neigh = vars(v).zipWithIndex.filter(_._1.nonEmpty).map(_._2).head
      and(vars(neigh)(v)(c.id), vars(v)(neigh)(c.id))
    }
  }


  def tHTransitionFilter(colors: Seq[Point]): Boolean = {
    val isomorphism = (colors(0).id, colors(1).id) match {
      case (0, 9) | (9, 0) | (0, 1) | (1, 0) | (1, 3) | (3, 1) | (3, 6) | (6, 3) |
           (1, 7) | (7, 1) | (0, 0) | (1, 1) => true
      case _ => false
    }

    val zeroSum = colors.map(_.value).reduce(_ ^ _) == 0

    isomorphism && zeroSum
  }
}
