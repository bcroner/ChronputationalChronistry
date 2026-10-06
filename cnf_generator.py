class CNFGenerator:
    """
    Generates standard DIMACS CNF boolean strings from MicroStar 
    mass stability constraints for the C++ EverythingEquationApp (EEA) engine.
    """
    def __init__(self, num_particles: int = 1, max_mass: int = 209):
        self.num_particles = num_particles
        self.max_mass = max_mass
        # Your explicit right-column unstable exceptions
        self.unstable_exceptions = {5, 8, 9, 107, 109, 147, 203, 205}
        
        # Tracking variables
        self.current_var_id = 1
        self.variable_map = {}
        self.clauses = []

    def get_var_id(self, label: str) -> int:
        """Retrieves or registers a unique integer ID for a boolean literal."""
        if label not in self.variable_map:
            self.variable_map[label] = self.current_var_id
            self.current_var_id += 1
        return self.variable_map[label]

    def build_mapping_schema(self):
        """Initializes the variable assignment mappings across the particle set."""
        for p in range(self.num_particles):
            # 1. Mass mapping: True if particle p has discrete mass m
            for m in range(1, self.max_mass + 1):
                self.get_var_id(f"P{p}_M{m}")
            # 2. Instability status mapping
            self.get_var_id(f"P{p}_Unstable")
            # 3. Fragmentation routine trigger mapping
            self.get_var_id(f"P{p}_Fragment")

    def generate_constraints(self):
        """Compiles the physical micro-star laws into 3SAT logical clauses."""
        for p in range(self.num_particles):
            unstable_var = self.get_var_id(f"P{p}_Unstable")
            fragment_var = self.get_var_id(f"P{p}_Fragment")

            # --- Rule A: Mass Uniqueness (A particle can only hold 1 mass state at a time) ---
            for m1 in range(1, self.max_mass + 1):
                v1 = self.get_var_id(f"P{p}_M{m1}")
                for m2 in range(m1 + 1, self.max_mass + 1):
                    v2 = self.get_var_id(f"P{p}_M{m2}")
                    # Clause: (NOT v1 OR NOT v2) -> DIMACS: -v1 -v2 0
                    self.clauses.append(f"-{v1} -{v2} 0")

            # --- Rule B: Instability Core (Explicit right-column mass exceptions force Unstable) ---
            for m in range(1, self.max_mass + 1):
                mass_var = self.get_var_id(f"P{p}_M{m}")
                if m in self.unstable_exceptions:
                    # Mass_m implies Unstable -> (NOT Mass_m OR Unstable)
                    self.clauses.append(f"-{mass_var} {unstable_var} 0")
                else:
                    # Stable mass implies NOT Unstable -> (NOT Mass_m OR NOT Unstable)
                    self.clauses.append(f"-{mass_var} -{unstable_var} 0")

            # --- Rule C: Fragmentation Routine (Unstable states force absolute fragmentation) ---
            # Unstable implies Fragment -> (NOT Unstable OR Fragment)
            self.clauses.append(f"-{unstable_var} {fragment_var} 0")

    def export_dimacs(self) -> str:
        """Formats the generated clauses into clean DIMACS CNF layout."""
        num_variables = self.current_var_id - 1
        num_clauses = len(self.clauses)
        
        header = f"p cnf {num_variables} {num_clauses}\n"
        comment = "c --- EEA Engine Auto-Generated CNF Constraints for Computational Chemistry Module ---\n"
        
        return header + comment + "\n".join(self.clauses)


if __name__ == "__main__":
    # Initialize generator for 1 sample particle structure
    generator = CNFGenerator(num_particles=1, max_mass=12) # Truncated mass step limit for small demo footprint
    generator.build_mapping_schema()
    generator.generate_constraints()
    
    # Render DIMACS output
    print(generator.export_dimacs())
