package service

import (
	"log"
	"os"
	"sync"
)

type XYService struct {
	client Client
}
type Client interface {
	SetRecord(courseId string) error
}

func NewXYService(client Client) *XYService {
	return &XYService{client: client}
}

func (s *XYService) RecordLearning() error {
	fin := make(chan struct{}, 100)
	done := make(chan os.Signal, 1)
	wg := &sync.WaitGroup{}

	task := func() {
		defer func() {
			fin <- struct{}{}
			wg.Done()
		}()
		err := s.client.SetRecord(courseId)
		if err != nil {
			log.Println(err)
			return
		}
	}
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go task()
	}
	for {
		select {
		case <-fin:
			wg.Add(1)
			go task()
		case <-done:
			wg.Wait()
			break
		}
	}
}
