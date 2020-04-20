package main

import (
	"fmt"
	"gopkg.in/square/go-jose.v2/json"
	"log"
	"net/http"
	"time"
)

func CheckAuth() Middleware {
	return func(f http.HandlerFunc) http.HandlerFunc {
		return func(w http.ResponseWriter, r *http.Request) {
			flag := true
			fmt.Println("Checking Auth")
			if flag {
				f(w, r)
			} else {
				return
			}
		}
	}
}
func Login() Middleware {
	return func(f http.HandlerFunc) http.HandlerFunc {
		return func(w http.ResponseWriter, r *http.Request) {
			start := time.Now()
			defer func() {
				log.Println(r.URL.Path, time.Since(start))
			}()
			f(w, r)
		}
	}
}

func AcceptedHosts() Middleware {
	return func(f http.HandlerFunc) http.HandlerFunc {
		return func(w http.ResponseWriter, r *http.Request) {
			IPAddress := r.Header.Get("X-Real-Ip")
			if IPAddress == "" {
				IPAddress = r.Header.Get("X-Forwarded-For")
			}
			if IPAddress == "" {
				IPAddress = r.RemoteAddr
			}

			res, _ := json.Marshal(map[string]string{
				"ip": IPAddress,
			})
			w.Header().Add("Content-Type", "application/json")
			w.Write(res)

			fmt.Println(IPAddress, res)
			var allowedHosts []string
			allowedHosts = append(allowedHosts, "http://localhost")
			allowedHosts = append(allowedHosts, "http://127.0.0.1")
			for i := 0; i < len(allowedHosts); i++ {
				if r.Host == allowedHosts[i] {
					f(w, r)
				}
			}

		}
	}
}
