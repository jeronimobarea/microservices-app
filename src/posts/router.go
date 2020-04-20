package main

import (
	"net/http"
)

type Router struct {
	/*
		This struct handle the routes and the methods of the server
		1º map[string] handles the type
		2º map[string] handles the url
	*/
	rules map[string]map[string]http.HandlerFunc
}

func NewRouter() *Router {
	/*
		Initialize a new route with the router struct
	*/
	return &Router{
		rules: make(map[string]map[string]http.HandlerFunc),
	}
}

func (r *Router) FindHandler(path string, method string) (http.HandlerFunc, bool, bool) {
	/*
		Find's if the requested path exists
	*/
	_, exist := r.rules[path]
	handler, methodExist := r.rules[path][method]
	return handler, methodExist, exist
}

func (r *Router) ServeHTTP(w http.ResponseWriter, request *http.Request) {
	/*
		Handles the path and method
	*/
	handler, methodExist, exist := r.FindHandler(request.URL.Path, request.Method)

	if !exist {
		w.WriteHeader(http.StatusNotFound)
		return
	}

	if !methodExist {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
	handler(w, request)
}
