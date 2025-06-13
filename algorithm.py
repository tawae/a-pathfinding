from queue import PriorityQueue

# Hàm heuristic tính khoảng cách Manhattan giữa hai điểm
# Manhattan = |x1 - x2| + |y1 - y2|
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Dựng lại đường đi từ điểm cuối về điểm đầu dựa vào dictionary came_from
# và gọi hàm draw() để cập nhật giao diện

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()  # Hang doi uu tien theo f-score
    open_set.put((0, count, start))  # f_score, count, node
    came_from = {}  # Đây là một dictionary để lưu vết đường đi

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}  # Để kiểm tra nhanh xem node đã trong hàng đợi chưa

    while not open_set.empty():
        current = open_set.get()[2] # Lay phan tu co f-score nho nhat
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True  # Tìm thấy đường

        # Xét các node lân cận
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # Mỗi bước đi có chi phí 1

            if temp_g_score < g_score[neighbor]:
                # Cap nhat duong di tot hon
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()  # Đánh dấu node đang xét

        draw()

        if current != start:
            current.make_closed()  # Đánh dấu đã xét

    return False  # Không tìm thấy đường