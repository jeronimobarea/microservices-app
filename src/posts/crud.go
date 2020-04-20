package main

import (
	"encoding/json"
	"golang.org/x/tools/go/ssa/interp/testdata/src/errors"
	"net/http"
)

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

func FilterOffersByCategory(page, perPage int, category string) ([]byte, error) {
	var mediaPost []MediaPost

	items := db.Offset(page).Limit(perPage).Where("is_service = ? AND job_type = ?", false, category).Find(&mediaPost).Value

	var count int
	_ = db.Table("media_posts").Count(&count)

	res, err := Paginate(page, perPage, items, count)

	if err != nil && res == nil {
		return nil, errors.New("Failed the pagination")
	}
	return res, nil
}

func FilterServicesByCategory(page, perPage int, category string) ([]byte, error) {
	var mediaPost []MediaPost

	items := db.Offset(page).Limit(perPage).Where("is_service = ? AND job_type = ?", true, category).Find(&mediaPost).Value

	var count int
	_ = db.Table("media_posts").Count(&count)

	res, err := Paginate(page, perPage, items, count)

	if err != nil && res == nil {
		return nil, errors.New("Failed the pagination")
	}
	return res, nil
}

func GetMediaPostQuery(page, perPage int) ([]byte, error) {
	/*
		This function get's the page and per page numbers and returns
	*/
	var mediaPost []MediaPost
	items := db.Offset(page).Limit(perPage).Find(&mediaPost).Value

	var count int
	_ = db.Table("media_posts").Count(&count)

	res, err := Paginate(page, perPage, items, count)

	if err != nil && res == nil {
		return nil, errors.New("Failed the pagination")
	}
	return res, nil
}

func GetMediaOffersQuery(page, perPage int) ([]byte, error) {
	var mediaPost []MediaPost

	items := db.Offset(page).Limit(perPage).Where("is_service = ?", false).Find(&mediaPost).Value

	var count int
	_ = db.Table("media_posts").Count(&count)

	res, err := Paginate(page, perPage, items, count)

	if err != nil && res == nil {
		return nil, errors.New("Failed the pagination")
	}
	return res, nil
}

func GetMediaServicesQuery(page, perPage int) ([]byte, error) {
	var mediaPost []MediaPost

	items := db.Offset(page).Limit(perPage).Where("is_service = ?", true).Find(&mediaPost).Value

	var count int
	_ = db.Table("media_posts").Count(&count)

	res, err := Paginate(page, perPage, items, count)

	if err != nil && res == nil {
		return nil, errors.New("Failed the pagination")
	}
	return res, nil
}

func GetUserMediaOffersQuery(page, perPage int, id string) ([]byte, error) {
	var mediaPost []MediaPost

	items := db.Offset(page).Limit(perPage).Where("is_service = ? AND creator_id = ?", false, id).Find(&mediaPost).Value

	var count int
	_ = db.Table("media_posts").Count(&count)

	res, err := Paginate(page, perPage, items, count)

	if err != nil && res == nil {
		return nil, errors.New("Failed the pagination")
	}
	return res, nil
}

func GetUserMediaServicesQuery(page, perPage int, id string) ([]byte, error) {
	var mediaPost []MediaPost

	items := db.Offset(page).Limit(perPage).Where("is_service = ? AND creator_id = ?", true, id).Find(&mediaPost).Value

	var count int
	_ = db.Table("media_posts").Count(&count)

	res, err := Paginate(page, perPage, items, count)

	if err != nil && res == nil {
		return nil, errors.New("Failed the pagination")
	}
	return res, nil
}

func GetMediaByIdQuery(id string) ([]byte, error) {
	var mediaPost MediaPost
	err := db.Find(&mediaPost).Where("id=?", id).Value
	if err != nil {
		return nil, errors.New("Error retrieving data from the table")
	}
	response, _ := mediaPost.ToJson()
	return response, nil
}

func PatchMediaPostQuery(id string, r *http.Request) ([]byte, error) {
	var mediaPost MediaPost
	err := db.Find(&mediaPost).Where("id=?", id)

	if err != nil {
		return nil, errors.New("Error retrieving data from the table")
	}

	var updated MediaPost
	decoder := json.NewDecoder(r.Body)
	_ = decoder.Decode(&updated)

	mediaPost.Description = updated.Description
	mediaPost.Title = updated.Title
	mediaPost.PaymentQuantity = updated.PaymentQuantity

	db.Save(mediaPost)
	response, _ := mediaPost.ToJson()

	return response, nil
}

func DeleteMediaObjectQuery(id string) error {
	var mediaPost MediaPost
	err := db.Where("id=?", id).Delete(&mediaPost)
	if err != nil {
		return errors.New("Could not find any object with that id")
	}
	return nil
}
