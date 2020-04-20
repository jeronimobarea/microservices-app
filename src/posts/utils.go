package main

import (
	"encoding/json"
	"golang.org/x/tools/go/ssa/interp/testdata/src/errors"
)

func Paginate(page, perPage int, items interface{}, count int) ([]byte, error) {
	/*
		This function handle the conversion and the data of the MediaPost struct to a paginated one
		page: page of the info
		perPage: number of items per page
		items: MediaPost un serialized data
		count: total items of the MediaPost table
	*/
	var mediaPost []MediaPost
	var pagination Pagination

	// Serialization of the []MediaPost
	response, err := json.Marshal(items)

	if err != nil {
		return nil, errors.New("Error serializing the data")
	}

	totalPages := count / perPage
	pagination.TotalPages = totalPages
	pagination.HasNext = totalPages > page
	pagination.HasPrev = page > 0
	_ = json.Unmarshal(response, &mediaPost)
	pagination.Results = mediaPost

	response, err = json.Marshal(pagination)

	return response, nil
}
