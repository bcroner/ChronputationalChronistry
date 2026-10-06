class IsotopeValidator:
    """
    Validates the structural viability of MicroStar masses
    based on the observed whole-number mass stability dataset.
    """
    def __init__(self):
        # Explicit exclusion zones: Whole numbers that are fundamentally unstable
        self.unstable_exceptions = {5, 8, 9, 107, 109, 147, 203, 205}
        
        # Max limit defined by the boundaries of your structural data
        self.max_stable_mass = 209

    def verify_mass_stability(self, mass_amu: float) -> bool:
        """
        Determines if a given mass configuration can exist stably over time.
        Non-integer masses and explicit right-column exceptions return False.
        """
        # 1. Scale-invariant check: Mass must be a discrete whole number unit
        if not mass_amu.is_integer():
            return False
            
        mass_int = int(mass_amu)
        
        # 2. Check if the mass falls outside our recorded upper limit
        if mass_int > self.max_stable_mass:
            return False
            
        # 3. Filter out the explicit unstable exceptions from the right column
        if mass_int in self.unstable_exceptions:
            return False
            
        # If it passes the exclusion checks, it represents a valid stable element core
        return True
