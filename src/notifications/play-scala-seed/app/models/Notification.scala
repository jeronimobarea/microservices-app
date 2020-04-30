package models

import java.util.UUID

import akka.http.scaladsl.model.DateTime

case class Notification(
    id: String,
    user: String,
    title: String,
    content: String,
    creationDate: Option[String]
)
