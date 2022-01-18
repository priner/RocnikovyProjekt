package com.matfyz.snarkmaster.configuration

case class Configuration(blocks: Set[Block]){
  def colors = blocks.flatMap(_.points)
}

case class Block(points: Set[Point])
case class Point(id: Int, value: Int)

object Block{
  def apply(p: Point*): Block = Block(p.toSet)

}

object Configuration{
  val thp0 = Point(0, 7)
  val thp1 = Point(1, 12)
  val thp2 = Point(2, 11)
  val thp3 = Point(3, 9)
  val thp4 = Point(4, 10)
  val thp5 = Point(5, 5)
  val thp6 = Point(6, 6)
  val thp7 = Point(7, 14)
  val thp8 = Point(8, 3)
  val thp9 = Point(9, 13)

  val THConfiguration = Configuration(Set(
    Block(thp0, thp1, thp2),
    Block(thp0, thp3, thp7),
    Block(thp0, thp4, thp9),
    Block(thp2, thp5, thp7),
    Block(thp2, thp6, thp9),
    Block(thp7, thp8, thp9)
  ))

  val extendedTHConfiguration = Configuration(Set(
    Block(thp0, thp1, thp2),
    Block(thp0, thp3, thp7),
    Block(thp0, thp4, thp9),
    Block(thp2, thp5, thp7),
    Block(thp2, thp6, thp9),
    Block(thp7, thp8, thp9),
    Block(thp1, thp3, thp5),
    Block(thp3, thp4, thp8),
    Block(thp5, thp6, thp8),
    Block(thp1, thp4, thp6)
  ))

  val THwithQuasiLine = Configuration(Set(
    Block(thp0, thp1, thp2),
    Block(thp0, thp3, thp7),
    Block(thp0, thp4, thp9),
    Block(thp2, thp5, thp7),
    Block(thp2, thp6, thp9),
    Block(thp7, thp8, thp9),
    Block(thp1, thp3, thp4)
  ))

  val threeColoring = Configuration(Set(Block(thp0,thp1,thp2)))

  val THAngleMid = Configuration(Set(
    Block(thp0, thp1, thp2),
    Block(thp0, thp3, thp7),
    Block(thp0, thp4, thp9),
    Block(thp2, thp5, thp7),
    Block(thp2, thp6, thp9),
    Block(thp7, thp8, thp9),
    Block(thp3, thp4, thp6)
  ))

  val THAngleCor = Configuration(Set(
    Block(thp0, thp1, thp2),
    Block(thp0, thp3, thp7),
    Block(thp0, thp4, thp9),
    Block(thp2, thp5, thp7),
    Block(thp2, thp6, thp9),
    Block(thp7, thp8, thp9),
    Block(thp3, thp4, thp2)
  ))

  sealed trait THFactors
  case object LineSegment extends THFactors
  case object MidPoint extends THFactors
  case object CornerPoint extends THFactors
  case object Angle extends THFactors
  case object HalfLine extends THFactors
  case object Axis extends THFactors
  case object Altitude extends THFactors

  val mids = Seq(1, 3, 4, 5, 6, 8)
  val corners = Seq(0, 2, 7, 9)

  def mapToFactor(t: (Point, Point)): THFactors = {
    val norm = if(t._1.id > t._2.id) t.swap else t
    (norm._1.id, norm._2.id) match {
      case (a, b) if a != b && corners.contains(a) && corners.contains(b) => LineSegment
      case (a, b) if a == b && mids.contains(a) => MidPoint
      case (a, b) if a == b && corners.contains(a) => CornerPoint
      case (1, 8) | (3, 6) | (4, 5) => Axis
      case (a, b) if mids.contains(a) && mids.contains(b) => Angle
      case (a, b) if THConfiguration.blocks.exists(x => x.points.map(_.id).contains(a) && x.points.map(_.id).contains(b)) => HalfLine
      case (a, b) if (mids.contains(a) && corners.contains(b)) || (mids.contains(b) && corners.contains(a)) &&
        !THConfiguration.blocks.exists(x => x.points.map(_.id).contains(a) && x.points.map(_.id).contains(b)) => Altitude

    }
  }
}


