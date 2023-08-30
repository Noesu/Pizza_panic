# Pizza Panic
# Player must catch falling pizzas before they hit the ground

# 1. Доработайте игру «Паника в пиццерии» так,
# чтобы сложность игрового процесса постепенно возрастала.
# 2. Задумайтесь о разных способах добиться следующих эффектов:
# - увеличить скорость падения пиццы и/или перемещения повара
# - уменьшить расстояние от крыши до сковороды
# - выпустить на экран нескольких сумасшедших кулинаров.

from superwires import games, color
import random

games.init(screen_width=640, screen_height=480, fps=50)


class Pan(games.Sprite):
    """
    A pan controlled by player to catch falling pizzas.
    """
    image = games.load_image("pan.bmp")

    """Задание исходного значения уровня и установка частоты повышения уровня"""
    game_level = 1
    levelup_list = []
    for i in range(0, 10000, 50):
        levelup_list.append(i)

    """Формирование списка уровней с увеличением скорости пиццы"""
    levels_with_pizza_speed_increase = []
    for i in range(0, 100, 3):
        levels_with_pizza_speed_increase.append(i)

    """Формирование списка уровней с увеличением скорости шефа"""
    levels_with_chef_speed_increase = []
    for i in range(0, 100, 5):
        levels_with_chef_speed_increase.append(i)

    """Формирование списка уровней с увеличением уровня сковороды"""
    levels_with_pan_position_change = []
    for i in range(0, 100, 5):
        levels_with_pan_position_change.append(i)

    """Формирование списка уровней с добавлением нового шефа"""
    levels_with_adding_extra_chef = []
    for i in range(0, 100, 5):
        levels_with_adding_extra_chef.append(i)

    def __init__(self):
        """ Initialize Pan object and create Text object for score. """
        super(Pan, self).__init__(image=Pan.image,
                                  x=games.mouse.x,
                                  bottom=games.screen.height)

        self.score = games.Text(value=0, size=25, color=color.black,
                                top=5, right=games.screen.width - 10)
        games.screen.add(self.score)

    def update(self):
        """ Move to mouse x position. """
        self.x = games.mouse.x

        if self.left < 0:
            self.left = 0

        if self.right > games.screen.width:
            self.right = games.screen.width

        self.check_catch()

    def check_catch(self):
        """ Check if catch pizzas. """
        for pizza in self.overlapping_sprites:
            self.score.value += 10
            self.score.right = games.screen.width - 10
            pizza.handle_caught()
            self.check_level()

    def check_level(self):
        """Проверка текущего количества очков на повышение уровня"""
        if self.score.value in self.levelup_list:
            self.level_up()

    def level_up(self):
        """Повышение уровня с выводом сообщения на экран."""
        self.game_level += 1
        if self.game_level in self.levels_with_pizza_speed_increase:
            Pizza.increase_speed()
        if self.game_level in self.levels_with_chef_speed_increase:
            Chef.increase_speed()
        if self.game_level in self.levels_with_pan_position_change:
            self.bottom -= 10
        if self.game_level in self.levels_with_adding_extra_chef:
            chef1 = Chef()
            games.screen.add(chef1)
        level_up_message = games.Message(value="LEVEL " + str(self.game_level),
                                         size=90,
                                         color=color.red,
                                         x=games.screen.width / 2,
                                         y=games.screen.height / 2,
                                         lifetime=1 * games.screen.fps,)
        games.screen.add(level_up_message)


class Pizza(games.Sprite):
    """
    A pizza which falls to the ground.
    """
    image = games.load_image("pizza.bmp")
    pizza_speed = 1

    def __init__(self, x, y=90):
        """ Initialize a Pizza object. """
        super(Pizza, self).__init__(image=Pizza.image,
                                    x=x, y=y,
                                    dy=Pizza.pizza_speed)

    def update(self):
        """ Check if bottom edge has reached screen bottom. """
        if self.bottom > games.screen.height:
            self.end_game()
            self.destroy()

    def handle_caught(self):
        """ Destroy self if caught. """
        self.destroy()

    @staticmethod
    def increase_speed():
        """Увеличение скорости падения пиццы"""
        Pizza.pizza_speed *= 1.3

    def end_game(self):
        """ End the game. """
        end_message = games.Message(value="Game Over",
                                    size=90,
                                    color=color.red,
                                    x=games.screen.width / 2,
                                    y=games.screen.height / 2,
                                    lifetime=5 * games.screen.fps,
                                    after_death=games.screen.quit)
        games.screen.add(end_message)


class Chef(games.Sprite):
    """
    A chef which moves left and right, dropping pizzas.
    """
    image = games.load_image("chef.bmp")
    chef_speed = 2

    def __init__(self, y=55, odds_change=200):
        """ Initialize the Chef object. """
        super(Chef, self).__init__(image=Chef.image,
                                   x=games.screen.width / 2,
                                   y=y,
                                   dx=Chef.chef_speed)

        self.odds_change = odds_change
        self.time_til_drop = 0

    def update(self):
        """ Determine if direction needs to be reversed. """
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        elif random.randrange(self.odds_change) == 0:
            self.dx = -self.dx

        self.check_drop()

    def check_drop(self):
        """ Decrease countdown or drop pizza and reset countdown. """
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_pizza = Pizza(x=self.x)
            games.screen.add(new_pizza)

            # set buffer to approx 30% of pizza height, regardless of pizza speed
            self.time_til_drop = int(new_pizza.height * 1.3 / Pizza.pizza_speed) + 1

    @staticmethod
    def increase_speed():
        """Увеличение скорости шефа"""
        Chef.chef_speed += 1
        Chef.dx = Chef.chef_speed


def main():
    """ Play the game. """
    wall_image = games.load_image("wall.jpg", transparent=False)
    games.screen.background = wall_image

    the_chef = Chef()
    games.screen.add(the_chef)

    the_pan = Pan()
    games.screen.add(the_pan)

    games.mouse.is_visible = False

    games.screen.event_grab = True
    games.screen.mainloop()


# start it up!
main()
