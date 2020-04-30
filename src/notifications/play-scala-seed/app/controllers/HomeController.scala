package controllers

import javax.inject._

import scala.concurrent.ExecutionContext.Implicits.global
import play.api._
import play.api.mvc._
import repositories.NotificationRepository

/**
  * This controller creates an `Action` to handle HTTP requests to the
  * application's home page.
  */
@Singleton
class HomeController @Inject()(
    cc: ControllerComponents,
    notificationRepository: NotificationRepository
) extends AbstractController(cc) {

  /**
    * Create an Action to render an HTML page.
    *
    * The configuration in the `routes` file means that this method
    * will be called when the application receives a `GET` request with
    * a path of `/`.
    */
  def index(): Action[AnyContent] = Action {
    implicit request: Request[AnyContent] =>
      Ok(views.html.index())
  }

  def dbInit(): Action[AnyContent] = Action.async { request =>
    notificationRepository.dbInit
      .map(_ => Created("Table created"))
      .recover { ex =>
        play.Logger.of("dbInit").debug("Error in dbInit", ex)
        InternalServerError(s"there was an error")
      }

  }

}
