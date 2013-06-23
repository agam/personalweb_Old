package agamsweb

import (
  "fmt"
	"net/http"
)

func init() {
	http.HandleFunc("/helloworld", notFoundHandler)
}

func notFoundHandler(w http.ResponseWriter, r *http.Request) {
  fmt.Fprintf(w, "<h1>Hello, World!</h1>");
}
