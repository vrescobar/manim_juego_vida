import manimlib
from manimlib import *
import sys
sys.path.insert(1, '.')

from life_game import Life
CUSTOM_BLACK = BLACK
_BLACK_OPACITY = 0.6
TITLE_FONT_SIZE = 60
BODY_FONT_SIZE = 30
TITLE_BODY_BUFFER = 0.4
FONT_FAMILY = 'Poppins'
# FONT_FAMILY = 'Verdana'


class AppLife(Scene):

    def construct(self) -> None:
        num_rows = 40
        # num_cols = 60
        num_cols = 72
        # crear un tablero de vida vacío
        self.life = Life(num_rows, num_cols)
        # esta cuadrícula será nuestro campo de juego para mostrar la animación de vida
        grid = AppLife.create_grid(num_rows, num_cols, cell_height=14)
        self.add(grid)

    @staticmethod
    def create_grid(num_rows, num_cols, cell_height=6):
        # crear una cuadrícula de cuadrados
        square = Square()
        square.set_fill(WHITE, opacity=_BLACK_OPACITY)
        square.set_stroke(GREY, width=0)

        grid = square.get_grid(num_rows, num_cols, height=cell_height)
        grid.arrange_in_grid(
            n_rows=num_rows,
            n_cols=num_cols,
            h_buff=0,
            v_buff=0
        )

        return grid

    def animate_grid(self, grid, life, num_generations, wait_time=0.1):
        # la primera iteración del bucle muestra el estado inicial del tablero
        # la segunda iteración muestra la siguiente generación

        # self.put_counter(wait_time)

        generation = 1
        while generation <= num_generations:
            self.wait(wait_time)

            # mostrar el estado actual en la pantalla
            # for i in range(life.num_rows):
            for i in range(len(life.board)):
                # for j in range(life.num_cols):
                for j in range(len(life.board[0])):

                    # la cuadrícula es una lista unidimensional (400,)
                    grid_idx = life.num_cols * i + j

                    # esta celda está viva
                    if life.board[i][j] == 1:
                        grid[grid_idx].set_fill(BLACK)
                        grid[grid_idx].set_stroke(BLACK, width=.3)
                    else:
                        grid[grid_idx].set_fill(WHITE, opacity=_BLACK_OPACITY)
                        grid[grid_idx].set_stroke(BLACK, width=.3)

            life.compute_next_state()
            generation += 1

    def show_title_n_body(self, title, body, wait_time=2.5):
        title = Text(title, font_size=TITLE_FONT_SIZE, font=FONT_FAMILY, color=BLACK)
        body = Text(body, font_size=BODY_FONT_SIZE, font=FONT_FAMILY, color=BLACK)
        vgroup = VGroup(title, body).arrange(
            DOWN, buff=TITLE_BODY_BUFFER, center=False, aligned_edge=LEFT)  # .set_y(0)
        vgroup.to_edge(UP)
        vgroup.to_edge(LEFT)
        self.play(FadeIn(vgroup))
        self.wait(wait_time)

    def show_text(self, text_str, font_size, wait_time=2.5):
        text = Text(text_str, font_size=font_size, font=FONT_FAMILY, color=BLACK)
        text.to_edge(UP)
        text.to_edge(LEFT)
        self.play(FadeIn(text))
        self.wait(wait_time)

    def show_question(self, wait_time=3):
        text = Text(
            "P: Dado un estado del tablero,\n¿es posible determinar si un cierto patrón desaparecerá o vivirá para siempre?",
            font_size=BODY_FONT_SIZE, font=FONT_FAMILY, color=BLACK)
        text.to_edge(UP)
        text.to_edge(LEFT)

        credits_text = Text("código original: github.com/emadehsan/life",
                            font_size=BODY_FONT_SIZE, font=FONT_FAMILY, color=BLACK)
        modificado = Text("Modificado por Víctor R. Escobar: https://github.com/vrescobar/manim_juego_vida",
                            font_size=BODY_FONT_SIZE, font=FONT_FAMILY, color=BLACK)
        credits_text.to_edge(BOTTOM)
        # modificado, just below credits
        modificado.next_to(credits_text, DOWN)
        
        text.to_edge(LEFT)

        self.play(FadeIn(text))
        self.wait(wait_time)
        self.play(FadeIn(modificado), FadeIn(credits_text))
        self.wait(wait_time)

    def show_rules(self, grid, life, wait_time=1.5):
        rules = [
            {
                "title": "Subpoblación",
                "body": "Una célula viva con menos de dos vecinos muere",
            },
            {
                "title": "Supervivencia",
                "body": "Una célula con dos o tres vecinos vive para la siguiente generación"
            },
            {
                "title": "Sobrepoblación",
                "body": "Una célula con más de tres vecinos muere"
            },
            {
                "title": "Reproducción",
                "body": "Una célula muerta con exactamente tres vecinos se convierte en una célula viva"
            }
        ]

        # las 4 funciones de life_game.py que establecen la configuración del tablero
        # para el ejemplo que muestra la regla aplicada
        board_state_functions = [
            life.put_underpopulation_example,
            life.put_survival_example,
            life.put_overpopulation_example,
            life.put_reproduction_example
        ]

        # índice del cuadrado en la cuadrícula. este es el cuadrado que se verá afectado en la próxima generación al jugar según la regla. para enfocar, hacer un destello
        # estos coinciden con los ejemplos de las funciones life.put_*_example
        flash_indexes = [
            (0, 4),  # esta célula morirá
            (-1, -1),  # sin cambios
            (1, 1),  # esto morirá
            (0, 1),  # esto cobrará vida
        ]

        for i, rule in enumerate(rules):
            # limpiar la pantalla y el tablero, borrar textos, etc.
            self.clear_screen(grid, life)

            # mostrar el texto de esta regla
            title = Text(
                rule['title'], font_size=TITLE_FONT_SIZE, font=FONT_FAMILY, color=BLACK)
            body = Text(rule['body'], font_size=BODY_FONT_SIZE,
                        font=FONT_FAMILY, color=BLACK)
            # body2 = Text(rule['body2'], font_size=BODY_FONT_SIZE, font=FONT_FAMILY, color=BLACK)

            vgroup = VGroup(title, body).arrange(
                DOWN, buff=TITLE_BODY_BUFFER, center=False, aligned_edge=LEFT)
            vgroup.to_edge(UP)
            vgroup.to_edge(LEFT)
            self.play(FadeIn(vgroup))

            # mostrar la animación de esta regla
            self.display_rule_example(
                grid, life, board_state_functions[i], flash_indexes[i])

            self.wait(wait_time)

    def clear_screen(self, grid, life):
        life.clear_board()  # esto borrará las células vivas

        # ahora animar la cuadrícula durante una generación,
        # esto hará que todos los cuadrados de la cuadrícula se muestren en gris (es decir, vacíos)
        self.animate_grid(grid, life, num_generations=1)

        # borrar texto y animación
        self.clear()

        # agregar nuevamente la cuadrícula de fondo (que ahora son todas células grises)
        self.add(grid)

    def glider(self, grid, life, num_generations, wait_time=0.1):
        life.clear_board()
        life.put_glider_at(life.num_rows//3, life.num_cols//3)

        self.animate_grid(grid, life, num_generations, wait_time)

    def glider_gun(self, grid, life, num_generations, wait_time=0.1):
        life.clear_board()
        life.put_glider_gun(life.num_rows//2 - 5, life.num_cols//5)

        self.animate_grid(grid, life, num_generations, wait_time)

    def display_rule_example(self, grid, life: Life, set_board_state_func, flash_index, wait_time=1) -> None:
        # poner el ejemplo en el centro. los ejemplos elegidos para resaltar cada regla
        # solo necesitan una generación de animación
        i = life.num_rows // 2 - 1
        j = life.num_cols // 2 - 1

        set_board_state_func(i, j)

        # animar durante 1 generación, esto mostrará el estado inicial del tablero para esta regla
        self.animate_grid(grid, life, num_generations=1, wait_time=wait_time)

        self.wait(wait_time)

        # agregar efecto de destello
        a, b = flash_index
        if a >= 0 and b >= 0:
            self.play(
                Flash(grid[
                    life.num_cols * (i+a) + (j+b)
                ], color=RED_A, flash_radius=0.4)
            )

        # animar durante 1 generación nuevamente, esto avanzará el estado del tablero por 1 generación
        self.animate_grid(grid, life, num_generations=1, wait_time=wait_time)

        self.wait(wait_time)

    def r_pentomino(self, grid, life, num_generations, wait_time=0.1):
        # poner el R-pentomino y animarlo
        life.clear_board()
        life.put_r_pentomino(life.num_rows//2, life.num_cols//2)

        self.animate_grid(grid, life, num_generations, wait_time)

    def put_counter(self, wait_time):
        # CountInFrom()

        # cuenta las generaciones
        # , text_config={"font": "monospace"})  #.scale(2)
        counter = DecimalNumber(1)
        # ChangingDecimal()

        def update_func(t):
            return t * 10

        counter.to_edge(UP)
        counter.to_edge(RIGHT)
        # counter.
        # ChangingDecimal()
        # self.add(counter)
        self.play(ChangingDecimal(counter, update_func), run_time=wait_time)

    def still_life(self, grid, life, num_generations, wait_time=0.2):
        life.clear_board()
        life.put_still_life()

        self.animate_grid(grid, life, num_generations, wait_time)

    def oscillators(self, grid, life, num_generations, wait_time=0.2):
        life.clear_board()
        life.put_oscillators()

        self.animate_grid(grid, life, num_generations, wait_time)

    def copperhead(self, grid, life, num_generations, wait_time=0.2):
        life.clear_board()
        life.put_copperhead(life.num_rows//2 - 4, life.num_cols//2 - 6)

        self.animate_grid(grid, life, num_generations, wait_time)

class SceneGlider(AppLife):
    def construct(self):
        super().construct()
        num_rows = 40
        num_cols = 72
        wait_time=0.1

        life = Life(num_rows, num_cols)
        grid = AppLife.create_grid(num_rows, num_cols, cell_height=14)
        self.add(grid)

        self.glider(grid, life, num_generations=30, wait_time=wait_time)

class SceneIntro(AppLife):
    def construct(self):
        super().construct()
        num_rows = 40
        num_cols = 72
        wait_time=2.5

        life = Life(num_rows, num_cols)
        grid = AppLife.create_grid(num_rows, num_cols, cell_height=14)
        self.add(grid)

        self.show_title_n_body(
            title="Juego de la Vida",
            body="El Juego de la Vida de Conway es un juego de cero jugadores con unas reglas simples",
            wait_time=wait_time,
        )

class SceneRules(AppLife):
    def construct(self):
        super().construct()
        num_rows = 40
        num_cols = 72
        wait_time=1.5

        life = Life(num_rows, num_cols)
        grid = AppLife.create_grid(num_rows, num_cols, cell_height=14)
        self.add(grid)

        self.show_rules(grid, life, wait_time=wait_time)

class ScenePostRules(AppLife):
    def construct(self):
        super().construct()
        num_rows = 40
        num_cols = 72
        wait_time=2.5

        life = Life(num_rows, num_cols)
        grid = AppLife.create_grid(num_rows, num_cols, cell_height=14)
        self.add(grid)

        self.clear_screen(grid, life)
        self.show_text("Estas reglas convierten patrones de inicio simples en patrones complejos.\n"
                       "Algunos desaparecen por completo y otros progresan infinitamente", font_size=BODY_FONT_SIZE, wait_time=wait_time)

class SceneRPentomino(AppLife):
    def construct(self):
        super().construct()
        num_rows = 40
        num_cols = 72

        life = Life(num_rows, num_cols)
        grid = AppLife.create_grid(num_rows, num_cols, cell_height=14)
        self.add(grid)

        self.clear_screen(grid, life)
        self.show_text("R-pentominó", font_size=TITLE_FONT_SIZE, wait_time=1)
        self.r_pentomino(grid, life, num_generations=1, wait_time=1)
        self.wait(0.5)

        self.r_pentomino(grid, life, num_generations=70)

class SceneStillLife(AppLife):
    def construct(self):
        super().construct()
        num_rows = 40
        num_cols = 72
        wait_time = 0.2

        life = Life(num_rows, num_cols)
        grid = AppLife.create_grid(num_rows, num_cols, cell_height=14)
        self.add(grid)

        self.clear_screen(grid, life)
        self.show_title_n_body("Vida Estática",
                               "Patrones que no cambian en las generaciones posteriores")

        self.still_life(grid, life, num_generations=15, wait_time=wait_time)

class SceneOscillators(AppLife):
    def construct(self):
        super().construct()
        num_rows = 40
        num_cols = 72
        wait_time = 0.3

        life = Life(num_rows, num_cols)
        grid = AppLife.create_grid(num_rows, num_cols, cell_height=14)
        self.add(grid)

        self.clear_screen(grid, life)
        self.show_title_n_body(
            "Osciladores", "Vuelven a su estado inicial después de algunas generaciones")

        self.oscillators(grid, life, num_generations=25, wait_time=wait_time)

class SceneGliderGun(AppLife):
    def construct(self):
        super().construct()
        num_rows = 40
        num_cols = 72
        wait_time = 1

        life = Life(num_rows, num_cols)
        grid = AppLife.create_grid(num_rows, num_cols, cell_height=14)
        self.add(grid)

        self.clear_screen(grid, life)
        self.show_title_n_body("Arma del Planeador de Gosper (Glider Gun)",
                               "Emite un planeador cada 30 generaciones (descubierto en 1970)")
        self.glider_gun(grid, life, num_generations=1, wait_time=wait_time)
        self.wait(0.5)

        self.glider_gun(grid, life, num_generations=90, wait_time=0.05)

class SceneCopperhead(AppLife):
    def construct(self):
        super().construct()
        num_rows = 40
        num_cols = 72
        wait_time = 1

        life = Life(num_rows, num_cols)
        grid = AppLife.create_grid(num_rows, num_cols, cell_height=14)
        self.add(grid)

        self.clear_screen(grid, life)
        self.show_title_n_body(
            "Cabeza de Cobre", "Nave espacial (descubierta en 2016)")
        self.copperhead(grid, life, num_generations=1, wait_time=wait_time)
        self.wait(0.5)

        self.copperhead(grid, life, num_generations=100, wait_time=0.1)

class SceneQuestion(AppLife):
    def construct(self):
        wait_time = 3
        self.show_question(wait_time=wait_time)

class SceneRandom(AppLife):
    def construct(self):
        super().construct()
        num_rows = 40
        num_cols = 72
        wait_time = 0.1

        life = Life(num_rows, num_cols)
        grid = AppLife.create_grid(num_rows, num_cols, cell_height=14)
        self.add(grid)

        life.random_board()
        self.animate_grid(grid, life, num_generations=30, wait_time=wait_time)
    
if __name__ == "__main__":
    SceneGlider().construct()
    SceneRandom().construct()
    SceneIntro().construct()
    SceneRules().construct()
    ScenePostRules().construct()
    SceneRPentomino().construct()
    SceneStillLife().construct()
    SceneOscillators().construct()
    SceneGliderGun().construct()
    SceneCopperhead().construct()
    SceneQuestion().construct()
