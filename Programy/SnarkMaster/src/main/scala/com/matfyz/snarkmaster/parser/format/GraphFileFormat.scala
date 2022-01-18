package com.matfyz.snarkmaster.parser.format

import java.io.File

import com.matfyz.snarkmaster.SnarkMasterException
import com.matfyz.snarkmaster.graph.{Component, Graph}

import scala.io.Source

trait GraphFileFormat {
  def parse(file: File): Seq[Graph] = {
    val in = Source.fromFile(file)

    val lines = in.getLines()

    parse(file, lines)
  }

  def parse(file: File, lines: Iterator[String]): Seq[Graph]
}

trait ComponentFileFormat {
  def parse(file: File): Seq[Component] = {
    val in = Source.fromFile(file)

    val lines = in.getLines()

    parse(file, lines)
  }

  def parse(file: File, lines: Iterator[String]): Seq[Component]
}