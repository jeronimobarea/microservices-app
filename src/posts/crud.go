package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"golang.org/x/tools/go/ssa/interp/testdata/src/errors"
)

// Revised
func MediaPostQuery(r *http.Request) ([]byte, error) {
	/*
		This function handles the decode of the request data and insert it to the database
	*/
	decoder := json.NewDecoder(r.Body)
	var mediaPost MediaPost

	err := decoder.Decode(&mediaPost)
	if err != nil {
		return nil, errors.New("Could not decode the data")
	}

	db.Create(&mediaPost)
	response, err := mediaPost.ToJson()

	if err != nil {
		return nil, errors.New("Could not parse to json")
	}

	return response, nil
}

// Revised
func FilterPostTypeByCategory(page, perPage int, postType, category string) ([]byte, error) {
	var mediaPost []MediaPost

	items := db.Offset(page).Limit(perPage).Where("post_type = ? AND category = ?", postType, category).Find(&mediaPost).Value

	mediaPost, err := FillUserData(mediaPost)

	var count int
	_ = db.Table("media_posts").Count(&count)

	res, err := Paginate(page, perPage, items, count)

	if err != nil && res == nil {
		return nil, errors.New("Failed the pagination")
	}
	return res, nil
}

// Revised
func GetMediaPostQuery(page, perPage int) ([]byte, error) {
	/*
		This function get's the page and per page numbers and returns
	*/
	var mediaPost []MediaPost
	items := db.Offset(page).Limit(perPage).Find(&mediaPost).Value

	mediaPost, err := FillUserData(mediaPost)

	var count int
	_ = db.Table("media_posts").Count(&count)

	res, err := Paginate(page, perPage, items, count)

	if err != nil && res == nil {
		return nil, errors.New("Failed the pagination")
	}
	return res, nil
}

// Revised
func GetMediaServicesQuery(page, perPage int, postType string) ([]byte, error) {
	var mediaPost []MediaPost

	items := db.Offset(page).Limit(perPage).Where("post_type = ?", postType).Find(&mediaPost).Value

	mediaPost, err := FillUserData(mediaPost)

	var count int
	_ = db.Table("media_posts").Count(&count)

	res, err := Paginate(page, perPage, items, count)

	if err != nil && res == nil {
		return nil, errors.New("Failed the pagination")
	}
	return res, nil
}

// Revised
func GetUserMediaFilterQuery(page, perPage int, postType, id string) ([]byte, error) {
	var mediaPost []MediaPost

	items := db.Offset(page).Limit(perPage).Where("post_type = ? AND creator_id = ?", postType, id).Find(&mediaPost).Value

	mediaPost, err := FillUserData(mediaPost)

	var count int
	_ = db.Table("media_posts").Count(&count)

	res, err := Paginate(page, perPage, items, count)

	if err != nil && res == nil {
		return nil, errors.New("Failed the pagination")
	}
	return res, nil
}

// Revised
func GetMediaByIdQuery(id string) ([]byte, error) {
	var mediaPost MediaPost
	_ = db.Where("id=?", id).Find(&mediaPost).Value

	if mediaPost.CreatorId == "" {
		return nil, errors.New("Invalid id")
	}

	req, err := http.Get("http://127.0.0.1:8100/profiles/basic/" + mediaPost.CreatorId)

	fmt.Println("http://127.0.0.1:8100/profiles/basic/" + mediaPost.CreatorId)
	if err != nil {
		fmt.Println(err)
		return nil, err

	}

	decoder := json.NewDecoder(req.Body)
	var userData UserData
	err = decoder.Decode(&userData)
	if err != nil {
		panic(err)
	}
	log.Println(userData)

	mediaPost.UserData.UserName = userData.UserName
	mediaPost.UserData.Image = userData.Image

	response, _ := mediaPost.ToJson()
	return response, nil
}

// Revised
func PatchMediaPostQuery(id string, r *http.Request) ([]byte, error) {
	var mediaPost MediaPost
	_ = db.Find(&mediaPost).Where("id=?", id)

	var updated MediaPost
	decoder := json.NewDecoder(r.Body)
	_ = decoder.Decode(&updated)

	mediaPost.Description = updated.Description
	mediaPost.Title = updated.Title
	mediaPost.PaymentQuantity = updated.PaymentQuantity
	mediaPost.Category = updated.Category
	mediaPost.LastModification = time.Now()

	db.Save(mediaPost)
	response, _ := mediaPost.ToJson()

	return response, nil
}

// Revised
func DeleteMediaObjectQuery(id string) error {
	var mediaPost MediaPost
	_ = db.Where("id=?", id).Delete(&mediaPost)
	return nil
}
