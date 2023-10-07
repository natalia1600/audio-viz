# Draw loop
while running:
    # Handle user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False

    # Update screen
    # draw_frame()


# Cleanup and exit
print("Goodbye!")
pygame.quit()