(defproject auth "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}
  :dependencies [[org.clojure/clojure "1.10.0"]
                 ; Compojure - A basic routing library
                 [compojure "1.6.1"]
                 ; Our Http library for client/server
                 [http-kit "2.3.0"]
                 ; Ring defaults - for query params etc
                 [ring/ring-defaults "0.3.2"]
                 ; Clojure data.JSON library
                 [org.clojure/data.json "0.2.6"]
                 ; Clojure http requests
                 [clj-http "3.10.1"]
                 ; Cheshire json parser
                 [cheshire "5.7.1"]
                 ; Ring json parser
                 [ring/ring-json "0.5.0"]]
  :main ^:skip-aot auth.core
  :repl-options {:init-ns auth.core})
