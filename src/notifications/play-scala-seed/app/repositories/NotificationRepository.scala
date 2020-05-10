package repositories

import javax.inject.Inject
import models.Notification
import play.api.db.slick.{DatabaseConfigProvider, HasDatabaseConfigProvider}
import play.api.mvc.{AbstractController, ControllerComponents}
import slick.jdbc.JdbcProfile
import slick.lifted.TableQuery
import tables.NotificationTable
import slick.jdbc.PostgresProfile.api._

import scala.concurrent.{ExecutionContext, Future}

class NotificationRepository @Inject()(
    protected val dbConfigProvider: DatabaseConfigProvider,
    cc: ControllerComponents
)(implicit ec: ExecutionContext)
    extends AbstractController(cc)
    with HasDatabaseConfigProvider[JdbcProfile] {

  private lazy val notificationQuery = TableQuery[NotificationTable]

  /**
    *
    * @return
    */
  def dbInit: Future[Unit] = {
    val createSchema = notificationQuery.schema.createIfNotExists
    db.run(createSchema)
  }

  def getAll: Future[Seq[Notification]] = {
    val q = notificationQuery.sortBy(_.id)
    db.run(q.result)
  }

  def getOne(id: String): Future[Option[Notification]] = {
    val q = notificationQuery.filter(_.id === id)
    db.run(q.result.headOption)
  }

  def getByUser(id: String): Future[Seq[Notification]] = {
    val q = notificationQuery.filter(_.user === id)
    db.run(q.result)
  }

  def create(notification: Notification): Future[Option[Notification]] = {
    val insert = notificationQuery += notification
    db.run(insert)
      .flatMap(_ => getOne(notification.id))
  }

  def update(id: String,
             notification: Notification): Future[Option[Notification]] = {
    val q = notificationQuery.filter(
      _.id === notification.id && notification.id.contains(id))
    val update = q.update(notification)
    db.run(update)
      .flatMap(_ => db.run(q.result.headOption))
  }

  def delete(id: String): Future[Option[Notification]] = {
    val q = notificationQuery.filter(_.id === id)

    for {
      notification <- db.run(q.result.headOption)
      _ <- db.run(q.delete)
    } yield notification
  }
}
