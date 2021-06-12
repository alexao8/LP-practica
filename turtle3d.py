import vpython as vp
import math


class Turtle3D:

    # Fer atributs per tots els constructors
    def __init__(self, x_pos=0.0, y_pos=0.0, z_pos=0.0, alpha=0.0, beta=0.0, color=vp.color.red, show_path=True, show_axis=False):

        # Posicio del turtle
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos

        # Direccio en la que mira el Turtle
        self.alpha = alpha
        self.beta = beta

        # Color en que es pintara
        self.color = color

        # Si ha de pintar o no al caminar
        self.show_path = show_path

        # Inicialitzem l'escena
        self._initialize_scene()

        # Pintem els eixos si s'han de mostrar
        if show_axis:
            self._print_axis()

    def forward(self, dist):
        self._move(dist)

    def backward(self, dist):
        self._move(-dist)

    def _move(self, dist):

        # Calculem el punt final
        x_dir, y_dir, z_dir = self._calculate_direction(self.alpha, self.beta, dist)
        x_dest = self.x_pos + x_dir
        y_dest = self.y_pos + y_dir
        z_dest = self.z_pos + z_dir

        # S'ha de pintar el cami
        if self.show_path:

            # Pintar cilindre
            vp.cylinder(pos=vp.vector(self.x_pos, self.y_pos, self.z_pos), axis=vp.vector(x_dir, y_dir, z_dir), radius=0.1, color=self.color)

            # Pintar esfera dels extrems
            vp.sphere(pos=vp.vector(self.x_pos, self.y_pos, self.z_pos), radius=0.1, color=self.color)
            vp.sphere(pos=vp.vector(x_dest, y_dest, z_dest), radius=0.1, color=self.color)

        # Assignar nova possicio
        self.x_pos = x_dest
        self.y_pos = y_dest
        self.z_pos = z_dest

    def left(self, grades):
        self._rotate_alpha(grades)

    def right(self, grades):
        self._rotate_alpha(-grades)

    def _rotate_alpha(self, grades):
        self.alpha += grades

    def up(self, grades):
        self._rotate_beta(grades)

    def down(self, grades):
        self._rotate_beta(-grades)

    def _rotate_beta(self, grades):
        self.beta += grades

    def show(self):
        self.show_path = True

    def hide(self):
        self.show_path = False

    def change_color(self, color_list):
        color = vp.vector(color_list[0], color_list[1], color_list[2])
        self.color = color

    def home(self):
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.z_pos = 0.0

    def _calculate_direction(self, alpha, beta, dist):
        x_dir = dist * math.cos(math.radians(alpha)) * math.cos(math.radians(beta))
        y_dir = dist * math.sin(math.radians(alpha)) * math.cos(math.radians(beta))
        z_dir = dist * math.sin(math.radians(beta))
        return x_dir, y_dir, z_dir

    def _initialize_scene(self):
        vp.scene.height = vp.scene.width = 1000
        vp.scene.autocenter = True
        vp.scene.caption = """\nTo rotate "camera", drag with right button or Ctrl-drag.\nTo zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.\n  On a two-button mouse, middle is left + right.\nTo pan left/right and up/down, Shift-drag.\nTouch screen: pinch/extend to zoom, swipe or two-finger rotate.\n"""

    def _print_axis(self):
        vp.cylinder(pos=vp.vector(0, 0, 0), axis=vp.vector(10, 0, 0), radius=0.1, color=vp.color.white)
        vp.cylinder(pos=vp.vector(0, 0, 0), axis=vp.vector(0, 10, 0), radius=0.1, color=vp.color.red)
        vp.cylinder(pos=vp.vector(0, 0, 0), axis=vp.vector(0, 0, 10), radius=0.1, color=vp.color.blue)
