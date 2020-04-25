package main

import (
	"encoding/json"
	"github.com/google/uuid"
	_ "github.com/google/uuid"
	"github.com/jinzhu/gorm"
	"net/http"
	"time"
)

type Middleware func(handlerFunc http.HandlerFunc) http.HandlerFunc

// Table declaration

type UserData struct {
	ID       string `json:"id"`
	Image    string `json:"image"`
	UserName string `json:"username"`
}

type MediaPost struct {
	ID               uuid.UUID `json:"id";gorm:"primary_key"`
	CreatorId        string    `json:"creator_id";gorm:"not null"`
	PostType         string      `json:"post_type";gorm:"not null"`
	Category         string    `json:"category";gorm:"not null"`
	Title            string    `json:"title";gorm:"not null"`
	Description      string    `json:"description";gorm:"not null"`
	PaymentQuantity  float32   `json:"payment_quantity"`
	CreationDate     time.Time `json:"creation_date"`
	LastModification time.Time `json:"last_modification"`
	UserData         UserData  `json:"user_data";gorm:"-"`
}

// Table functions declaration
func (m *MediaPost) BeforeCreate(scope *gorm.Scope) error {
	_ = scope.SetColumn("ID", uuid.New())
	_ = scope.SetColumn("CreationDate", time.Now())
	_ = scope.SetColumn("LastModification", time.Now())
	return nil
}

func (m *MediaPost) ToJson() ([]byte, error) {
	return json.Marshal(m)
}

// Pagination struct
type Pagination struct {
	Page       int         `json:"page"`
	TotalPages int         `json:"total_pages"`
	HasNext    bool        `json:"has_next"`
	HasPrev    bool        `json:"has_prev"`
	Results    []MediaPost `json:"results"`
}
