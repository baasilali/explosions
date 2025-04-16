"""
Physics-based Ball Explosion Simulation

This module implements a physics-based simulation of a ball that explodes upon impact
with a wall. The simulation features:
- Realistic physics with gravity and elastic collisions
- Velocity-based explosion effects
- Interactive user interface with velocity input
- Ball-to-ball collision detection and response
- Energy loss through bounce damping

The simulation uses Tkinter for the GUI and implements a simple 2D physics engine
for ball movement and collisions.

Author: Baasil Ali
Date: April 16th, 2025
"""

import tkinter as tk
import math
import random

# Global simulation parameters
velocity = 0  # Current ball velocity
balls = []    # List of active main balls
explosion_balls = []  # List of explosion particles
BALL_RADIUS = 10  # Radius of the main ball in pixels
EXPLOSION_BALL_RADIUS = 5  # Radius of explosion particles in pixels
GRAVITY = 0.5  # Gravity acceleration in pixels/frame²
BOUNCE_FACTOR = 0.7  # Energy retention factor for bounces (0-1)

# Initialize the main window
window = tk.Tk()
window.title("Physics Ball Explosion Simulator")
window.geometry("500x500")

# Create the drawing canvas
canvas = tk.Canvas(window, width=500, height=500, bg='white')
canvas.place(x=0, y=30)

# UI Elements
label = tk.Label(window, text="Enter Velocity: ")
label.place(x = 5, y = 0)

txtField = tk.Text(window, height = 1, width = 10)
txtField.place(x = 100, y = 3)

def validate_integer(event=None):
    """
    Validates that the input in the text field is a valid integer.
    
    Args:
        event: Optional event object from Tkinter binding
        
    Returns:
        bool: True if input is valid integer, False otherwise
        
    Side Effects:
        Displays error message if validation fails
    """
    try:
        value = txtField.get("1.0", tk.END).strip()
        if value and not value.isdigit():
            warn_label = tk.Label(window, text="Integers only!", fg="red")
            warn_label.place(x = 5, y = 25)
            window.after(2000, warn_label.destroy)
            return False
        return True
    except Exception:
        return False

def refresh_simulation():
    """
    Resets the simulation to its initial state.
    
    Clears all balls, the canvas, and the input field.
    """
    global balls, explosion_balls
    balls.clear()
    explosion_balls.clear()
    canvas.delete("all")
    txtField.delete("1.0", tk.END)

def throw_ball(event=None):
    """
    Creates and launches a new ball with the specified velocity.
    
    Args:
        event: Optional event object from Tkinter binding
        
    Side Effects:
        Creates a new ball if input is valid
        Displays error message if input is invalid
    """
    if not validate_integer():
        return
    txtContent = txtField.get("1.0", tk.END).strip()
    global velocity
    try:
        velocity = int(txtContent)
        balls.append(Ball(50, 250, velocity, 0, BALL_RADIUS, 'red'))
    except Exception:
        warn_label = tk.Label(window, text="Invalid input", fg="red")
        warn_label.place(x = 5, y = 25)
        window.after(2000, warn_label.destroy)

# Bind Enter key to throw_ball function
txtField.bind('<Return>', throw_ball)

# Create button container and buttons
button_frame = tk.Frame(window)
button_frame.place(x=180, y=-1)

throw_button = tk.Button(button_frame, text="Throw", command=throw_ball)
throw_button.pack(side=tk.LEFT, padx=5)

refresh_button = tk.Button(button_frame, text="Refresh", command=refresh_simulation)
refresh_button.pack(side=tk.LEFT, padx=5)

class Ball:
    """
    Represents a ball in the simulation with physical properties and behavior.
    
    Attributes:
        x (float): X-coordinate of ball center
        y (float): Y-coordinate of ball center
        dx (float): X-component of velocity
        dy (float): Y-component of velocity
        radius (float): Ball radius in pixels
        color (str): Ball color in hex format
    """
    
    def __init__(self, x, y, dx, dy, radius, color):
        """
        Initialize a new ball with position, velocity, and appearance.
        
        Args:
            x (float): Initial x-coordinate
            y (float): Initial y-coordinate
            dx (float): Initial x-velocity
            dy (float): Initial y-velocity
            radius (float): Ball radius
            color (str): Ball color
        """
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius
        self.color = color

    def move(self):
        """
        Update ball position based on current velocity and gravity.
        
        Applies gravity to y-velocity and updates position based on velocity components.
        """
        self.x += self.dx
        self.y += self.dy
        self.dy += GRAVITY

    def draw(self):
        """
        Draw the ball on the canvas.
        
        Creates an oval shape representing the ball at its current position.
        """
        canvas.create_oval(self.x - self.radius, self.y - self.radius,
                         self.x + self.radius, self.y + self.radius,
                         fill=self.color)

def check_collision(ball1, ball2):
    """
    Check if two balls are colliding.
    
    Args:
        ball1 (Ball): First ball
        ball2 (Ball): Second ball
        
    Returns:
        bool: True if balls are colliding, False otherwise
    """
    distance = math.sqrt((ball1.x - ball2.x)**2 + (ball1.y - ball2.y)**2)
    return distance < (ball1.radius + ball2.radius)

def handle_collision(ball1, ball2):
    """
    Handle elastic collision between two balls.
    
    Implements elastic collision physics using conservation of momentum
    and energy principles.
    
    Args:
        ball1 (Ball): First ball
        ball2 (Ball): Second ball
    """
    # Calculate collision normal
    dx = ball1.x - ball2.x
    dy = ball1.y - ball2.y
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance == 0:
        return
        
    # Normalize collision vector
    dx /= distance
    dy /= distance
    
    # Calculate relative velocity
    dvx = ball1.dx - ball2.dx
    dvy = ball1.dy - ball2.dy
    
    # Calculate impulse (2 * relative velocity dot normal)
    impulse = 2 * (dvx * dx + dvy * dy) / 2
    
    # Apply impulse to both balls
    ball1.dx -= impulse * dx
    ball1.dy -= impulse * dy
    ball2.dx += impulse * dx
    ball2.dy += impulse * dy

def create_explosion(x, y, velocity):
    """
    Create explosion particles at the specified location.
    
    Args:
        x (float): X-coordinate of explosion center
        y (float): Y-coordinate of explosion center
        velocity (float): Initial velocity of main ball (affects particle count)
    """
    # Number of particles proportional to velocity
    num_particles = int(velocity / 2)
    
    for _ in range(num_particles):
        # Random angle and speed for each particle
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(velocity * 0.2, velocity * 0.4)
        
        # Calculate velocity components
        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed
        
        # Random color for visual effect
        color = f'#{random.randint(0, 0xFFFFFF):06x}'
        
        # Create and add particle
        explosion_balls.append(Ball(x, y, dx, dy, EXPLOSION_BALL_RADIUS, color))

def update():
    """
    Main update loop for the simulation.
    
    Handles:
    - Ball movement and drawing
    - Wall collisions
    - Ball-to-ball collisions
    - Explosion creation
    - Particle cleanup
    
    This function is called approximately 60 times per second.
    """
    canvas.delete("all")
    
    # Update and draw main ball
    for ball in balls:
        ball.move()
        ball.draw()
        
        # Handle wall collisions
        if ball.x + ball.radius > 500:  # Right wall
            ball.x = 500 - ball.radius
            ball.dx *= -BOUNCE_FACTOR
            create_explosion(ball.x, ball.y, velocity)
            balls.remove(ball)
        elif ball.x - ball.radius < 0:  # Left wall
            ball.x = ball.radius
            ball.dx *= -BOUNCE_FACTOR
        if ball.y + ball.radius > 500:  # Bottom wall
            ball.y = 500 - ball.radius
            ball.dy *= -BOUNCE_FACTOR
        elif ball.y - ball.radius < 0:  # Top wall
            ball.y = ball.radius
            ball.dy *= -BOUNCE_FACTOR
    
    # Update and draw explosion particles
    for ball in explosion_balls:
        ball.move()
        ball.draw()
        
        # Handle wall collisions for particles
        if ball.x + ball.radius > 500:
            ball.x = 500 - ball.radius
            ball.dx *= -BOUNCE_FACTOR
        elif ball.x - ball.radius < 0:
            ball.x = ball.radius
            ball.dx *= -BOUNCE_FACTOR
        if ball.y + ball.radius > 500:
            ball.y = 500 - ball.radius
            ball.dy *= -BOUNCE_FACTOR
        elif ball.y - ball.radius < 0:
            ball.y = ball.radius
            ball.dy *= -BOUNCE_FACTOR
    
    # Check and handle collisions between explosion particles
    for i in range(len(explosion_balls)):
        for j in range(i + 1, len(explosion_balls)):
            if check_collision(explosion_balls[i], explosion_balls[j]):
                handle_collision(explosion_balls[i], explosion_balls[j])
    
    # Remove particles that have lost most of their energy
    explosion_balls[:] = [ball for ball in explosion_balls 
                         if abs(ball.dx) > 0.1 or abs(ball.dy) > 0.1]
    
    # Schedule next update (approximately 60 FPS)
    window.after(16, update)

# Start the animation loop
update()
window.mainloop()

