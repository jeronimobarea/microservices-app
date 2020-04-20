package main

import (
	"net/http"
)

// Server struct for the config
type Server struct {
	port   string
	router *Router
}

func NewServer(port string) *Server {
	/*
		This function returns a server with the config passed in the params
	*/
	return &Server{
		port:   port,
		router: NewRouter(),
	}
}

func (s *Server) Handle(method string, path string, handler http.HandlerFunc) {
	/*
		The Handle func handle's all the server routes.
		method: Http method that the route is handling (GET, POST...)
		path: The url path of the method
		handler: http function for execute the queries in that url
	*/
	_, exist := s.router.rules[path]
	if !exist {
		s.router.rules[path] = make(map[string]http.HandlerFunc)
	}
	s.router.rules[path][method] = handler
}

func (s *Server) AddMiddleware(f http.HandlerFunc, middlewares ...Middleware) http.HandlerFunc {
	/*
		This function add all the middleware functions that are in the middleware.go file
	*/
	for _, m := range middlewares {
		f = m(f)
	}
	return f
}

func (s *Server) Listen() error {
	/*
		This function starts the server
	 */
	http.Handle("/", s.router)
	err := http.ListenAndServe(s.port, nil)
	if err != nil {
		return err
	}
	return nil
}
