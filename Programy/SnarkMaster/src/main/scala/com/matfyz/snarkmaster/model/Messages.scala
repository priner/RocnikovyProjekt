package com.matfyz.snarkmaster.model

import java.io.File

import com.matfyz.snarkmaster.configuration.Configuration
import com.matfyz.snarkmaster.graph.{Component, Graph}
import com.matfyz.snarkmaster.parser.format.{ComponentFileFormat, GraphFileFormat}
import com.matfyz.snarkmaster.test.{SnarkTestResult, StartComponentTestMessage, StartTestMessage}

sealed trait Message

sealed trait ControlPanelMessage extends Message
case class TestGraphs(graphs: Seq[Graph], configuration: Configuration, tests: Seq[StartTestMessage]) extends ControlPanelMessage
case class TestComponents(component: Seq[Component], configuration: Configuration, tests: Seq[StartComponentTestMessage]) extends ControlPanelMessage
case class StartTestGraphs(tests: Seq[StartTestMessage]) extends ControlPanelMessage

case class ParseGraph(file: File, format: GraphFileFormat) extends Message
case class ParseComponent(file: File, format: ComponentFileFormat) extends Message

case class ParsedGraphs(graphs: Seq[Graph], file: File) extends Message
case class ParsedComponents(graphs: Seq[Component], file: File) extends Message

sealed trait LogMessage extends Message
case class LogText(msg: String) extends LogMessage
case class LogException(msg: String, cause: Option[Throwable] = None) extends LogMessage
case class LogResult(results: Seq[SnarkTestResult]) extends LogMessage