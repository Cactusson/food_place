import pygame as pg


left_col_middle = (50, 250)
left_col_bottom = (50, 500)
middle_col_top = (400, 150)
middle_col_middle = (400, 250)
middle_col_bottom = (400, 500)
right_col_top = (750, 150)
right_col_middle = (750, 250)
right_col_bottom = (750, 500)
left_table_col_top = (200, 150)
left_table_col_middle = (200, 250)
left_table_col_bottom = (200, 500)
right_table_col_top = (600, 150)
right_table_col_middle = (600, 250)
right_table_col_bottom = (600, 500)
washbox_entry = (275, 150)
orderbox_entry = (450, 150)
meal_1_entry = (550, 150)
meal_2_entry = (650, 150)
ufo_entry = (400, 450)


class Circle(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.image = self.create_image()
        self.rect = self.image.get_rect(center=center)

    def create_image(self):
        image = pg.Surface((30, 30)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        pg.draw.circle(image, pg.Color('purple'), (15, 15), 15)
        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Board:
    def __init__(self, tables_bool):
        # tables_bool should be like
        # [TOPLEFT, TOPRIGHT, BOTTOMLEFT, BOTTOMRIGHT]

        self.make_rows()
        self.create_graph(tables_bool)
        self.make_positions()
        self.circles = pg.sprite.Group()
        self.create_circles()

    def make_rows(self):
        left_col = [left_col_middle, left_col_bottom]
        middle_col = [
            middle_col_top, middle_col_middle, ufo_entry, middle_col_bottom]
        right_col = [right_col_top, right_col_middle, right_col_bottom]
        left_table_col = [
            left_table_col_top, left_table_col_middle,
            left_table_col_bottom]
        right_table_col = [
            right_table_col_top, right_table_col_middle,
            right_table_col_bottom]
        top_row = [
            left_table_col_top, washbox_entry,
            middle_col_top, orderbox_entry, meal_1_entry,
            right_table_col_top, meal_2_entry, right_col_top]
        middle_row = [
            left_col_middle, left_table_col_middle,
            middle_col_middle, right_table_col_middle,
            right_col_middle]
        bottom_row = [
            left_col_bottom, left_table_col_bottom,
            middle_col_bottom, right_table_col_bottom, right_col_bottom]

        # maybe it's not a good idea to have table cols full even
        # when there are not really connected
        self.rows = [
            left_col, middle_col, right_col, left_table_col, right_table_col,
            top_row, middle_row, bottom_row]

    def create_graph(self, tables_bool):
        self.graph = {

            left_col_middle: [
                left_col_bottom, left_table_col_middle,
                middle_col_middle, right_table_col_middle, right_col_middle],
            left_col_bottom: [
                left_col_middle, left_table_col_bottom,
                middle_col_bottom, right_table_col_bottom, right_col_bottom],

            left_table_col_top: [
                left_table_col_middle, washbox_entry,
                middle_col_top, orderbox_entry, meal_1_entry,
                right_table_col_top, meal_2_entry, right_col_top],
            left_table_col_middle: [
                left_table_col_top, left_col_middle, middle_col_middle,
                right_table_col_middle, right_col_middle],
            left_table_col_bottom: [
                left_col_bottom, middle_col_bottom, right_table_col_bottom,
                right_col_bottom],

            middle_col_top: [
                middle_col_middle, ufo_entry, middle_col_bottom,
                left_table_col_top, washbox_entry, orderbox_entry,
                meal_1_entry, right_table_col_top, meal_2_entry,
                right_col_top],
            middle_col_middle: [
                middle_col_top, ufo_entry, middle_col_bottom, left_col_middle,
                left_table_col_middle, right_table_col_middle,
                right_col_middle],
            ufo_entry: [
                middle_col_top, middle_col_middle, middle_col_bottom],
            middle_col_bottom: [
                middle_col_top, middle_col_middle, ufo_entry, left_col_bottom,
                left_table_col_bottom, right_table_col_bottom,
                right_col_bottom],

            right_table_col_top: [
                right_table_col_middle, left_table_col_top, washbox_entry,
                middle_col_top, orderbox_entry, meal_1_entry, meal_2_entry,
                right_col_top],
            right_table_col_middle: [
                right_table_col_top, left_col_middle, left_table_col_middle,
                middle_col_middle, right_col_middle],
            right_table_col_bottom: [
                left_col_bottom, left_table_col_bottom, middle_col_bottom,
                right_col_bottom],

            right_col_top: [
                right_col_middle, right_col_bottom, left_table_col_top,
                washbox_entry, middle_col_top, orderbox_entry,
                meal_1_entry, right_table_col_top, meal_2_entry],
            right_col_middle: [
                right_col_top, right_col_bottom, left_col_middle,
                left_table_col_middle, middle_col_middle,
                right_table_col_middle],
            right_col_bottom: [
                right_col_top, right_col_middle, left_col_bottom,
                left_table_col_bottom, middle_col_bottom,
                right_table_col_bottom],

            washbox_entry: [
                left_table_col_top, middle_col_top, orderbox_entry,
                meal_1_entry, right_table_col_top,
                meal_2_entry, right_col_top],
            orderbox_entry: [
                left_table_col_top, washbox_entry,
                middle_col_top, meal_1_entry, right_table_col_top,
                meal_2_entry, right_col_top],
            meal_1_entry: [
                left_table_col_top, washbox_entry,
                middle_col_top, orderbox_entry, right_table_col_top,
                meal_2_entry, right_col_top],
            meal_2_entry: [
                left_table_col_top, washbox_entry,
                middle_col_top, orderbox_entry, meal_1_entry,
                right_table_col_top, right_col_top]
        }

        if not tables_bool[0]:
            self.graph[left_table_col_top].append(left_table_col_bottom)
            self.graph[left_table_col_middle].append(left_table_col_bottom)
            self.graph[left_table_col_bottom].append(left_table_col_top)
            self.graph[left_table_col_bottom].append(left_table_col_middle)
        if not tables_bool[1]:
            self.graph[right_table_col_top].append(right_table_col_bottom)
            self.graph[right_table_col_middle].append(right_table_col_bottom)
            self.graph[right_table_col_bottom].append(right_table_col_top)
            self.graph[right_table_col_bottom].append(right_table_col_middle)

    def make_positions(self):
        self.waiter_pos = orderbox_entry
        self.washbox_pos = washbox_entry[0], washbox_entry[1] - 50
        self.washbox_entry = washbox_entry
        self.orderbox_pos = orderbox_entry[0], orderbox_entry[1] - 100
        self.orderbox_entry = orderbox_entry
        self.stand_pos = right_table_col_top[0], right_table_col_top[1] - 50
        self.meal_1_entry = meal_1_entry
        self.meal_2_entry = meal_2_entry
        self.table_positions = [left_table_col_middle, right_table_col_middle,
                                left_table_col_bottom, right_table_col_bottom]
        self.ufo_pos = ufo_entry
        self.firearm_pos = middle_col_top
        self.robber_pos = right_col_top

    def ufo_arrived_corrections(self):
        self.graph[ufo_entry].remove(middle_col_top)
        self.graph[ufo_entry].remove(middle_col_middle)
        self.graph[middle_col_bottom].remove(middle_col_top)
        self.graph[middle_col_bottom].remove(middle_col_middle)
        self.graph[middle_col_top].remove(ufo_entry)
        self.graph[middle_col_top].remove(middle_col_bottom)
        self.graph[middle_col_middle].remove(ufo_entry)
        self.graph[middle_col_middle].remove(middle_col_bottom)

    def ufo_departed_corrections(self):
        self.graph[ufo_entry].extend([middle_col_top, middle_col_middle])
        self.graph[middle_col_bottom].extend(
            [middle_col_top, middle_col_middle])
        self.graph[middle_col_top].extend([ufo_entry, middle_col_bottom])
        self.graph[middle_col_middle].extend([ufo_entry, middle_col_bottom])

    def create_circles(self):
        for point in self.graph.keys():
            circle = Circle(point)
            self.circles.add(circle)

    def get_point(self, pos):
        for circle in self.circles:
            if circle.rect.collidepoint(pos):
                return circle.rect.center

    def get_path(self, start, target):
        paths = []
        stack = [(start, [], [], 0)]
        min_distance = None

        while stack:
            current, visited, path, distance = stack.pop()
            if current == target:
                if min_distance is None:
                    min_distance = distance
                paths.append((distance, path))
            neighbors = self.graph[current]
            for neighbor in neighbors:
                new_visited = []
                for row in self.rows:
                    if current in row and neighbor in row:
                        new_visited.extend(row)
                if neighbor not in visited:
                    dist = (((current[0] - neighbor[0]) ** 2 +
                            (current[1] - neighbor[1]) ** 2) ** 0.5)
                    dist += distance
                    if min_distance is not None:
                        if dist <= min_distance:
                            stack.append(
                                (neighbor, list(set(visited + new_visited)),
                                 path + [neighbor], dist))
                    else:
                        stack.append(
                            (neighbor, list(set(visited + new_visited)),
                             path + [neighbor], dist))

        paths.sort()
        # candidates = [p for p in paths if p[0] == paths[0][0]]
        # return random.choice(candidates)[1]
        return paths[0][1]

    def draw(self, surface):
        for circle in self.circles:
            circle.draw(surface)
