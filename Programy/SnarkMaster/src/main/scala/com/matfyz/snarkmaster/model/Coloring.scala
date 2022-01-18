package com.matfyz.snarkmaster.model

import com.matfyz.snarkmaster.graph.Edge

case class Coloring(f: Edge => Int) {
  def apply(e: Edge): Int = f(e)
}
