package com.matfyz.snarkmaster.test

import com.matfyz.snarkmaster.configuration.Configuration
import com.matfyz.snarkmaster.graph.{Component, Graph}

case object StartTransitionExistTest extends StartComponentTestMessage {
  override def start(components: Seq[Component], configuration: Configuration) = {
    components.flatMap { component =>
      SATColoringTest.test(component.graph, configuration) match {
        case WithoutColoring(graph) => Seq(TransitionDoesntExists(graph, configuration))
        case ColoringExists(coloring, graph) =>
          //  println(coloring.mkString("\n"))
          Seq(TransitionExists(graph, configuration))
        case _ => throw new Exception("implementation error")
      }
    }
  }
}