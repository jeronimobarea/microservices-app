(ns auth.core
  (:require [org.httpkit.server :as server]
            [compojure.core :refer :all]
            [compojure.route :as route]
            [ring.middleware.defaults :refer :all]
            [clojure.pprint :as pp]
            [clojure.string :as str]
            [clojure.data.json :as json]
            [clj-http.client :as client]
            [cheshire.core]
            [ring.middleware.json :refer [wrap-json-body]]
            [auth.constants :refer [api-key server-path]])
  (:gen-class))


(defn login [req]
  (def email (get-in req [:body "email"]))
  (def password (get-in req [:body "password"]))
  (def url (str (server-path) "pr/profiles/email/" email))
  (try
    (def login-response (client/get url
                                    {:accept     :json
                                     :basic-auth [email password]
                                     :headers    {"api_key"      (api-key)
                                                  "Content-Type" "application/json"}}))
    (def profile-data (:body login-response))
    (catch Exception e (throw e)))
  {:status  200
   :headers {"Content-Type" "application/json"}
   :body    profile-data})

(defn create-user [req]
  (def email (get-in req [:body "email"]))
  (def password (get-in req [:body "password"]))
  (def device_id (get-in req [:body "device_id"]))
  (def data (:body req))

  (def consumer (cheshire.core/generate-string {:username email}))
  (def consumer-auth (cheshire.core/generate-string {:username email :password password}))
  (def profile (cheshire.core/generate-string {:email email :device_id device_id}))


  (try
    (def consumer-response (client/post (str (server-path) "auth/consumers/")
                                        {:accept  :json
                                         :headers {"api_key"      (api-key)
                                                   "Content-Type" "application/json"}
                                         :body    consumer}))

    (def final-url (str (server-path) "auth/consumers/" email url "/basic-auth"))

    (def auth-response (client/post final-url
                                    {:accept  :json
                                     :headers {"api_key"      (api-key)
                                               "Content-Type" "application/json"}
                                     :body    consumer-auth}))

    (def profile-response (client/post (str (server-path) "pr/profiles/")
                                       {:accept     :json
                                        :basic-auth [email password]
                                        :headers    {"api_key"      (api-key)
                                                     "Content-Type" "application/json"}
                                        :body       profile}))

    (def profile-data (:body profile-response))
    (catch Exception e (throw e)))
  {:status  200
   :headers {"Content-Type" "application/json"}
   :body    profile-data})


(defroutes app-routes
           (POST "/register" [] create-user)
           (POST "/login" [] login)
           (route/not-found "Error, page not found!"))
(defn -main
  "This is our main entry point"
  [& args]

  (let [port (Integer/parseInt (or (System/getenv "PORT") "3002"))]
    ; Run the server with Ring.defaults middleware
    (server/run-server (wrap-json-body #'app-routes (assoc-in site-defaults [:security :anti-forgery] false)) {:port port})
    ; Run the server without ring defaults
    ;(server/run-server #'app-routes {:port port})
    (println (str "Running webserver at http:/127.0.0.1:" port "/"))))

