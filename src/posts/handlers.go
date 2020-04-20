package main

import (
	_ "github.com/jinzhu/gorm/dialects/postgres"
	"net/http"
	"strconv"
)

func GetMediaService(w http.ResponseWriter, r *http.Request) {
	pageStr := r.URL.Query().Get("page")
	perPageStr := r.URL.Query().Get("per_page")

	var page int
	var perPage int

	if pageStr == "" || perPageStr == "" {
		page = 0
		perPage = 10
	} else {
		page, _ = strconv.Atoi(pageStr)
		perPage, _ = strconv.Atoi(perPageStr)
	}

	response, err := GetMediaServicesQuery(page, perPage)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write(response)
}

func GetMediaOffers(w http.ResponseWriter, r *http.Request) {
	pageStr := r.URL.Query().Get("page")
	perPageStr := r.URL.Query().Get("per_page")

	var page int
	var perPage int

	if pageStr == "" || perPageStr == "" {
		page = 0
		perPage = 10
	} else {
		page, _ = strconv.Atoi(pageStr)
		perPage, _ = strconv.Atoi(perPageStr)
	}

	response, err := GetMediaOffersQuery(page, perPage)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write(response)
}

func GetUserMediaOffers(w http.ResponseWriter, r *http.Request) {
	pageStr := r.URL.Query().Get("page")
	perPageStr := r.URL.Query().Get("per_page")
	id := r.URL.Query().Get("id")

	var page int
	var perPage int

	if pageStr == "" || perPageStr == "" {
		page = 0
		perPage = 10
	} else {
		page, _ = strconv.Atoi(pageStr)
		perPage, _ = strconv.Atoi(perPageStr)
	}

	response, err := GetUserMediaOffersQuery(page, perPage, id)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write(response)
}

func GetUserMediaServices(w http.ResponseWriter, r *http.Request) {
	pageStr := r.URL.Query().Get("page")
	perPageStr := r.URL.Query().Get("per_page")
	id := r.URL.Query().Get("id")

	var page int
	var perPage int

	if pageStr == "" || perPageStr == "" {
		page = 0
		perPage = 10
	} else {
		page, _ = strconv.Atoi(pageStr)
		perPage, _ = strconv.Atoi(perPageStr)
	}

	response, err := GetUserMediaServicesQuery(page, perPage, id)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write(response)
}

func GetOffersFilteredMedia(w http.ResponseWriter, r *http.Request) {
	pageStr := r.URL.Query().Get("page")
	perPageStr := r.URL.Query().Get("per_page")
	category := r.URL.Query().Get("category")

	var page int
	var perPage int

	if pageStr == "" || perPageStr == "" {
		page = 0
		perPage = 10
	} else {
		page, _ = strconv.Atoi(pageStr)
		perPage, _ = strconv.Atoi(perPageStr)
	}

	response, err := FilterOffersByCategory(page, perPage, category)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write(response)
}

func GetServicesFilteredMedia(w http.ResponseWriter, r *http.Request) {
	pageStr := r.URL.Query().Get("page")
	perPageStr := r.URL.Query().Get("per_page")
	category := r.URL.Query().Get("category")

	var page int
	var perPage int

	if pageStr == "" || perPageStr == "" {
		page = 0
		perPage = 10
	} else {
		page, _ = strconv.Atoi(pageStr)
		perPage, _ = strconv.Atoi(perPageStr)
	}

	response, err := FilterServicesByCategory(page, perPage, category)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write(response)
}

func MediaPostRequest(w http.ResponseWriter, r *http.Request) {
	/*
		This function create's a media object
	*/
	response, err := MediaPostQuery(r)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write(response)
}

func MediaUpdateRequest(w http.ResponseWriter, r *http.Request) {
	/*
		This function update's a media object
	*/
	id := r.URL.Query().Get("id")

	if id == "" {
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	response, err := PatchMediaPostQuery(id, r)

	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write(response)
}

func GetMediaPost(w http.ResponseWriter, r *http.Request) {
	/*
		This function handles to get all the posts
	*/
	pageStr := r.URL.Query().Get("page")
	perPageStr := r.URL.Query().Get("per_page")

	var page int
	var perPage int

	if pageStr == "" || perPageStr == "" {
		page = 0
		perPage = 10
	} else {
		page, _ = strconv.Atoi(pageStr)
		perPage, _ = strconv.Atoi(perPageStr)
	}

	res, err := GetMediaPostQuery(page, perPage)

	if err != nil && res == nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write(res)
}

func GetMediaById(w http.ResponseWriter, r *http.Request) {
	/*
		This function handles to get a post by his id
	*/
	id := r.URL.Query().Get("id")

	if id == "" {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	response, err := GetMediaByIdQuery(id)

	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write(response)
}

func DeleteMediaObject(w http.ResponseWriter, r *http.Request) {
	/*
		This function delete's a media object by his id
	*/
	id := r.URL.Query().Get("id")

	if id == "" {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	err := DeleteMediaObjectQuery(id)

	if err != nil {
		w.WriteHeader(http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write([]byte("Object eliminated"))
}
