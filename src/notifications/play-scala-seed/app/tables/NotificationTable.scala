package tables

import slick.jdbc.PostgresProfile.api._
import models.Notification

class NotificationTable(tag: Tag) extends Table[Notification](tag, "notifications") {
  def id = column[String]("id", O.PrimaryKey)

  def user = column[String]("user")

  def title = column[String]("title")

  def content = column[String]("content")

  def creationDate = column[String]("creation_date")

  def * =
    (id, user, title, content, creationDate.?) <> (Notification.tupled, Notification.unapply)
}
