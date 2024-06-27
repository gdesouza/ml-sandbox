# Games

## Move Square Static

### Description

The goal is to move the blue square into the red square without touching the borders of the screen.

The initial positions are fixed and there are no obstacles.

### Class Diagram
> _Install Markdown Preview to see the diagrams in VS Code_

```mermaid

classDiagram
    Game o-- Display
    Game : start()
    Game : is_game_ended()
    Game : success()
    Game : fail()
    Game : render()

    Display o-- Screen
    Screen : width
    Screen : height
    Screen : background_colour
    
    Display o-- Rectangle

    Display : is_car_inside_parking()
    Display : is_car_out_of_bounds()

    Rectangle : move()
    Rectangle : go_to()


```
