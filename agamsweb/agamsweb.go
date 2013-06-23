package agamsweb

import (
	"io/ioutil"
	"net/http"
)

func init() {
	http.HandleFunc("/", indexHandler)
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
  index, _ := ioutil.ReadFile("static/html/index.html")
  w.Write([]byte(index))
}
