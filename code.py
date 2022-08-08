import cv2
from pyzbar import pyzbar
import webbrowser
import platform

def read_barcodes(frame):
    barcode_info = ''
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        with open("barcode_result.txt", mode ='w') as file:
            file.write("Recognized Barcode:" + barcode_info)
    return frame, barcode_info


def main():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()

    if platform.system().lower() == "linux" or platform.system().lower() == "linux2":
        # Linux
        browser_path = '/usr/bin/google-chrome %s'
    elif platform.system().lower() == "darwin":          
        # MacOS
        browser_path = 'open -a /Applications/Google\ Chrome.app %s'
    elif platform.system().lower() == "win32":             
        # Windows
        browser_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    else:
        print('Could not detect OS')
        exit
    
    while ret:
        ret, frame = camera.read()
        frame, barcode_info = read_barcodes(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        if barcode_info:
            print(barcode_info)
            webbrowser.get(browser_path).open(barcode_info)
            break
        if cv2.waitKey(1) & 0xFF == 27:
            break
        
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()