import cv2
import numpy as np

# Biến toàn cục lưu điểm chuột
points = []
width, height = 400, 300  # Kích thước ảnh sau biến đổi

def get_perspective(event, x, y, flags, param):
    """Hàm callback để lấy tọa độ khi click chuột"""
    global points
    if event == cv2.EVENT_LBUTTONDOWN:  # Click chuột trái
        points.append((x, y))
        print(f"Đã chọn điểm: {x}, {y}")

cap = cv2.VideoCapture(0)  # Mở camera

cv2.namedWindow("Camera")
cv2.setMouseCallback("Camera", get_perspective)  # Gán sự kiện chuột

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Vẽ các điểm đã chọn lên khung hình
    for point in points:
        cv2.circle(frame, point, 5, (0, 0, 255), -1)

    # Nếu đã chọn đủ 4 điểm, thực hiện biến đổi phối cảnh
    if len(points) == 4:
        pts1 = np.float32(points)  # Chuyển danh sách điểm về numpy array
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

        # Tính toán ma trận biến đổi phối cảnh
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        
        # Áp dụng biến đổi
        transformed_frame = cv2.warpPerspective(frame, matrix, (width, height))

        cv2.imshow("Perspective Transform", transformed_frame)  # Hiển thị kết quả

    cv2.imshow("Camera", frame)  # Hiển thị camera gốc

    # Nhấn 'r' để reset điểm chọn, 'q' để thoát
    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):  # Reset điểm đã chọn
        points = []
    elif key == ord('q'):  # Thoát chương trình
        break

cap.release()
cv2.destroyAllWindows()
