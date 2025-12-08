import cv2
from ultralytics import YOLO

# ---- NASTAVENÍ ----
MODEL_PATH = "runs/detect/train/weights/best.pt"  # cesta k modelu
TARGET_CLASS = 0  # index třídy, kterou chceš počítat (0 = první třída)
# --------------------

# načtení modelu
model = YOLO(MODEL_PATH)

# otevření kamery
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Nelze otevřít kameru!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # inference
    results = model(frame, stream=True)

    # počítadlo detekcí
    count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])  # třída objektu
            if cls == TARGET_CLASS:
                count += 1

                # vykreslení bounding boxů
                x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                conf = float(box.conf[0])
                label = f"cps {conf:.2f}" # label = f"Class {cls} {conf:.2f}" # 

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # vykreslení počitadla
    cv2.putText(frame,
                f"Pocet objektu: {count} cps", # f"Počet objektů (class {TARGET_CLASS}): {count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                3)

    # zobraz video
    cv2.imshow("Detekce tobolek v reálném čase", frame)

    # ukončení klávesou Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
