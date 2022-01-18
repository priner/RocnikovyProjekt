package com.matfyz.snarkmaster.ui

import java.awt.event.{ActionEvent, ActionListener}
import javax.swing.JFileChooser

import akka.actor.{Actor, ActorRef}
import akka.event.LoggingReceive
import com.matfyz.snarkmaster.configuration.Configuration
import com.matfyz.snarkmaster.graph.Graph
import com.matfyz.snarkmaster.model._
import com.matfyz.snarkmaster.parser.format.TripleGraphFormat
import com.matfyz.snarkmaster.test._

class RemovabilityTabActor(uIActor: ActorRef, mainForm: MainForm) extends Actor{
  var graphs: Seq[Graph] = Nil

  override def receive: Receive = LoggingReceive{
    case m: ParsedGraphs =>
      graphs = m.graphs
      mainForm.graphInputRemovability.setText(m.file.getName)
      uIActor ! LogText("Parsed graphs from " + m.file.getName)
    case r: Seq[SnarkTestResult] =>
      //  mainForm.coloringTestStatus.setText("")
      uIActor ! LogResult(r)
    case _ =>
  }

  mainForm.selectGraphButtonRemovability.addActionListener(new ActionListener() {
    def actionPerformed(e: ActionEvent): Unit = {
      val fileChooser = new JFileChooser()
      fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY)
      fileChooser.showOpenDialog(mainForm.tabbedPane1)
      if(fileChooser.getSelectedFile != null)
        uIActor ! ParseGraph(fileChooser.getSelectedFile, TripleGraphFormat)
    }
  })

  mainForm.startRemovableVerticesTestButton.addActionListener(new ActionListener() {
    def actionPerformed(e: ActionEvent): Unit = {
      val configuration = Configuration.THConfiguration
      if (graphs.isEmpty) {
        uIActor ! LogException("Select graph")
      } else {
        uIActor ! TestGraphs(graphs, configuration, Seq(StartRemovableVerticesTest))
      }
    }
  })

  mainForm.startRemovablePairsOfVerticesTestButton.addActionListener(new ActionListener() {
    def actionPerformed(e: ActionEvent): Unit = {
      val configuration = Configuration.THConfiguration
      if (graphs.isEmpty) {
        uIActor ! LogException("Select graph")
      } else {
        uIActor ! TestGraphs(graphs, configuration, Seq(StartRemovablePairOfVerticesTest))
      }
    }
  })

  mainForm.startRemovableEdgesTestButton.addActionListener(new ActionListener() {
    def actionPerformed(e: ActionEvent): Unit = {
      val configuration = Configuration.THConfiguration
      if (graphs.isEmpty) {
        uIActor ! LogException("Select graph")
      } else {
        uIActor ! TestGraphs(graphs, configuration, Seq(StartRemovableEdgesTest))
      }
    }
  })

  mainForm.startRemovablePairsOfEdgesTestButton.addActionListener(new ActionListener() {
    def actionPerformed(e: ActionEvent): Unit = {
      val configuration = Configuration.THConfiguration
      if (graphs.isEmpty) {
        uIActor ! LogException("Select graph")
      } else {
        uIActor ! TestGraphs(graphs, configuration, Seq(StartRemovablePairOfEdgesTest))
      }
    }
  })

}

object RemovabilityTabActor{
  val actorName = "removability-tab"
}
