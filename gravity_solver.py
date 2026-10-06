import math

class GravitySolver:
    """
    Handles classical N-body gravitational calculations for our 
    scale-free chemistry engine.
    """
    def __init__(self, G_constant: float = 1.0):
        # We can scale the gravitational constant G to match the dimensions 
        # of our micro-space and accelerated time-dilation factor
        self.G = G_constant 

    def calculate_acceleration(self, body_a_pos: list, body_b_pos: list, body_b_mass: float) -> list:
        """Calculates the acceleration vector exerted on Body A by Body B."""
        # Calculate displacement vector
        dx = body_b_pos[0] - body_a_pos[0]
        dy = body_b_pos[1] - body_a_pos[1]
        dz = body_b_pos[2] - body_a_pos[2]
        
        # Distance squared with a small softening factor to avoid infinite forces at 0 distance
        dist_sq = dx**2 + dy**2 + dz**2 + 1e-9
        dist = math.sqrt(dist_sq)
        
        # Newtonian gravitational acceleration magnitude: a = G * M_b / r^2
        acc_mag = (self.G * body_b_mass) / dist_sq
        
        # Breakdown into directional unit vectors
        ax = acc_mag * (dx / dist)
        ay = acc_mag * (dy / dist)
        az = acc_mag * (dz / dist)
        
        return [ax, ay, az]

    def update_system(self, stars: list, planets: list, dt: float):
        """
        Advances the entire micro-solar system by one time step (dt)
        using a basic Verlet or Euler integration scheme.
        """
        # 1. Update Planet (Electron) Positions based on Star gravity
        for planet in planets:
            total_ax, total_ay, total_az = 0.0, 0.0, 0.0
            for star in stars:
                if not star.is_active:
                    continue
                ax, ay, az = self.calculate_acceleration(planet.position, [0,0,0], star.mass) # assuming star at origin for simplicity or track star.pos
                total_ax += ax
                total_ay += ay
                total_az += az
            
            # Update planetary velocities
            planet.velocity[0] += total_ax * dt
            planet.velocity[1] += total_ay * dt
            planet.velocity[2] += total_az * dt
            
            # Update planetary positions
            planet.position[0] += planet.velocity[0] * dt
            planet.position[1] += planet.velocity[1] * dt
            planet.position[2] += planet.velocity[2] * dt
