#include <iostream>
#include <SDL2/SDL.h>

int main(int argc, char** argv)
{
	// Just to make sure SDL is working
	SDL_Init(SDL_INIT_EVERYTHING);

	std::cout << "Hello World!" << std::endl;

	SDL_Quit();
	return 0;
}