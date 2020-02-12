package api

import "os"

func DeleteFile(filename string) {
	os.Remove(filename)
}
