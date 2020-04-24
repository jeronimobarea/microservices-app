package main

import (
	"fmt"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/postgres"
)

// Global var for database connection
var db *gorm.DB

func main() {
	// Initialize the database var and don't handle the error with _
	db, _ =
		GetDatabaseConnection("localhost", "app_posts", "app", "12345678A", 5432)
	fmt.Println("Successfully connected!")

	// Handle the database tables
	if db.Table("media_posts") == nil {
		db.Table("media_posts").CreateTable(&MediaPost{})
	}
	//db.Table("media_posts").CreateTable(&MediaPost{})

	/*
		Here we handle de server port, the routes and initialize the server
	*/
	server := NewServer(":3000")
	server.Handle("GET", "/posts", GetMediaPost)
	server.Handle("PATCH", "/post", MediaUpdateRequest)
	server.Handle("POST", "/posts", MediaPostRequest)
	server.Handle("GET", "/post", GetMediaById)
	server.Handle("DELETE", "/post", DeleteMediaObject)
	server.Handle("GET", "/posts/services", GetMediaService)
	server.Handle("GET", "/posts/offers", GetMediaOffers)
	server.Handle("GET", "/posts/offers/user", GetUserMediaOffers)
	server.Handle("GET", "/posts/services/user", GetUserMediaServices)
	server.Handle("GET", "/posts/offers/category", GetOffersFilteredMedia)
	server.Handle("GET", "/posts/services/category", GetServicesFilteredMedia)
	_ = server.Listen()
}
