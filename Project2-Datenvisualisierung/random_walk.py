from random import choice

class Randomwalk():
    """A class to generate random walks."""
    def __init__(self, num_points = 5000):
        self.num_points = num_points

        # Alle Bewegungen beginnen bei (0, 0).
        self.x_values = [0]
        self.y_values = [0]
    def fill_walk(self):
        """Calculate all the points in the walk."""

        # Fuerht Schritte aus, bis der Pfad die angegebene Laenge erreicht hat.
        while len(self.x_values) < self.num_points:
            # Waehlt die Richtung und die Weglaenge in dieser Richtung aus.
            x_step = self.get_stepx()
            y_step = self.get_stepy()

            # Lehnt Bewegungen ab, die nicht vom Fleck fuehren.
            if x_step == 0 and y_step == 0:
                continue

            # Berechnet den naechsten x- und y-Wert.
            x = self.x_values[-1] + x_step
            y = self.y_values[-1] + y_step

            self.x_values.append(x)
            self.y_values.append(y)
    def get_stepx(self):
            
            x_direction = choice([1, -1])

            x_distance = choice([0, 1, 2, 3, 4])
            return x_direction * x_distance
    def get_stepy(self):
            y_direction = choice([1, -1])
            y_distance = choice([1, 2, 3, 4])
            return y_direction * y_distance