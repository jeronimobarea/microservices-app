package controllers

import javax.inject._
import models.Notification
import play.Logger
import play.api.mvc._
import play.api.libs.json.{JsValue, Json, OFormat}
import repositories.NotificationRepository

import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

/**
  * This controller creates an `Action` to handle HTTP requests to the
  * application's home page.
  */
@Singleton
class NotificationController @Inject()(
    cc: ControllerComponents,
    notificationRepository: NotificationRepository
) extends AbstractController(cc) {

  implicit val serializer: OFormat[Notification] = Json.format[Notification]
  val logger: Logger.ALogger = play.Logger.of("NotificationController")

  /**
  * Methods
  */
  def getNotifications: Action[AnyContent] = Action.async {
    notificationRepository.getAll
      .map(notifications => {
        val j = Json.obj("data" -> notifications, "message" -> "Notifications listed")
        Ok(j)
      })
      .recover {
        case ex =>
          logger.error("Failed at getNotifications", ex)
          InternalServerError(
            s"An error has occurred ${ex.getLocalizedMessage}")
      }
  }

  def getUserNotifications(id: String): Action[AnyContent] = Action.async {
    notificationRepository
      .getByUser(id)
      .map(notifications => {
        val j = Json.obj("data" -> notifications, "message" -> "Notifications listed")
        Ok(j)
      })
      .recover {
        case ex =>
          logger.error("Failed at getUserNotifications", ex)
          InternalServerError(
            s"An error has occurred ${ex.getLocalizedMessage}")
      }
  }

  def getNotification(id: String): Action[AnyContent] = Action.async {
    notificationRepository
      .getOne(id)
      .map(notification => {
        val j = Json.obj("data" -> notification, "message" -> "Notification listed")
        Ok(j)
      })
      .recover {
        case ex =>
          logger.error("Failed at getNotification", ex)
          InternalServerError(
            s"An error has occurred ${ex.getLocalizedMessage}")
      }
  }

  def createNotification: Action[JsValue] = Action.async(parse.json) { request =>
    val validator = request.body.validate[Notification]

    validator.asEither match {
      case Left(error) => Future.successful(BadRequest(error.toString()))
      case Right(notification) => {
        notificationRepository
          .create(notification)
          .map(notification => {
            val j = Json.obj("data" -> notification, "message" -> "Notification created")
            Ok(j)
          })
          .recover {
            case ex =>
              logger.error("Failed at createNotification", ex)
              InternalServerError(
                s"An error has occurred ${ex.getLocalizedMessage}")
          }
      }
    }

  }

  def updateMovie(id: String): Action[JsValue] = Action.async(parse.json) {
    request =>
      val validator = request.body.validate[Notification]

      validator.asEither match {
        case Left(error) => Future.successful(BadRequest(error.toString()))
        case Right(notification) => {
          notificationRepository
            .update(id, notification)
            .map(notification => {
              val j = Json.obj("data" -> notification, "message" -> "Notification updated")
              Ok(j)
            })
            .recover {
              case ex =>
                logger.error("Failed at updateNotification", ex)
                InternalServerError(
                  s"An error has occurred ${ex.getLocalizedMessage}")
            }
        }
      }

  }

  def deleteNotification(id: String): Action[AnyContent] = Action.async {
    notificationRepository
      .delete(id)
      .map(notification => {
        val j = Json.obj("data" -> notification, "message" -> "Notification deleted")
        Ok(j)
      })
      .recover {
        case ex =>
          logger.error("Failed at deleteNotification", ex)
          InternalServerError(s"An error has occurred ${ex.getLocalizedMessage}")
      }
  }

}
