package com.matfyz.snarkmaster.solver

import java.io.{BufferedWriter, File, FileWriter, OutputStreamWriter}

import sat.formulas.{CNF, Formula, Var}

import scala.io.Source
import sys.process._

class LingelingSolver() {
  def solve(vars: Set[Var], cnf: CNF): Option[Set[Var]] = {
    val (cnfString, intToVar, _) = CNF.toDIMACS(cnf)

    val input = File.createTempFile("cnf","in")
    val fw = new FileWriter(input)
    val writer = new BufferedWriter(fw)

    val out = File.createTempFile("cnf","out")

    //writer.write(s"p cnf ${vars.size} ${cnf.clauses.size}\n")
    writer.write(cnfString)
    writer.flush()
    writer.close()
    fw.close()

    //println(cnfString)

    // println(s"lingeling ${input.getAbsolutePath} > ${out.getAbsolutePath}")

    try {
      Seq("/bin/sh", "-c", s"lingeling ${input.getAbsolutePath} > ${out.getAbsolutePath}").!!
    } catch {
      case _: Exception =>
    }

    input.delete()

    val output = Source.fromFile(out)
    val res = output.getLines().toList

    output.close()
    out.delete()



    if(res.contains("s UNSATISFIABLE")){
      None
    } else {
      val trueVars = res
        .filter(_.startsWith("v"))
        .flatMap{ line =>
          line.split(" ")
            .tail
            .filter(x => !x.startsWith("-") && x != "0")
            .map(v => intToVar(v.toInt))
        }
      Some(trueVars.toSet)
    }
  }
}
