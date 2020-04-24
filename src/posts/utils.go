package main

import (
	"fmt"

	"bytes"
	"encoding/json"
	"golang.org/x/tools/go/ssa/interp/testdata/src/errors"
	"net/http"
)

func FillUserData(mediaPost []MediaPost) ([]MediaPost, error) {
	/*

	 */
	var mediaId []string

	for _, m := range mediaPost {
		mediaId = append(mediaId, m.CreatorId)
	}

	result, _ := json.Marshal(&mediaId)

	req, err := http.NewRequest("GET", "http://127.0.0.1:8100/profiles/basic/list/", bytes.NewBuffer(result))

	client := &http.Client{}
	resp, err := client.Do(req)

	if err != nil {
		fmt.Println(err)
		return nil, errors.New("error making the request")
	}
	defer resp.Body.Close()

	decoder := json.NewDecoder(resp.Body)
	var userData []UserData
	err = decoder.Decode(&userData)

	if err != nil {
		fmt.Println(err)
		return nil, errors.New("error parsing the request")
	}

	for i := 0; i < len(mediaPost); i++ {
		for j := 0; j < len(userData); j++ {
			if i > len(userData) {
				j = 0
			}
			if mediaPost[i].CreatorId == userData[j].ID {
				mediaPost[i].UserData = userData[j]
			}
		}
	}

	return mediaPost, nil
}

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
