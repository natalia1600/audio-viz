CXX = g++
CXXFLAGS = -std=c++11

all: main

hello: main.cpp
	$(CXX) $(CXXFLAGS) -o hello main.cpp

clean:
	rm -f main
