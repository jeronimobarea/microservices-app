package main

import (
	"fmt"
	"github.com/jinzhu/gorm"

	_ "github.com/jinzhu/gorm/dialects/postgres"
)

func GetDatabaseConnection(host, dbName, user, password string, port int) (*gorm.DB, error) {
	/*
		Function that handles the database connection through gorm
	 */
	return gorm.Open("postgres", fmt.Sprintf("host=%s port=%d user=%s dbname=%s password=%s sslmode=disable",
		host, port, user, dbName, password))
}
