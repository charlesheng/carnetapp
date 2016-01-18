import cv2

def capture(img_file):

	video = cv2.VideoCapture(0)

	while True:
		ret, im = video.read()
		p1 = (140, -1)
		p2 = (140 + 360, 480)
		cv2.rectangle(im, p1, p2, (255, 255, 255), thickness=2)
		
		cv2.imshow('Mi Camara Fotografica', im)
		key = cv2.waitKey(10)

		if key%256 == 27:    # Esc key to stop
			break
		elif key%256 == ord(' ') or key%256 == 141 or key%256 == 10:    # Capture the image
			cv2.imwrite(img_file, im)
			cv2.imshow('Mi Foto Capturada', im)
		elif key == -1:  # normally -1 returned,so don't print it
			continue
		else:
			print 'You pressed %d (0x%x), LSB: %d (%s)' % (key, key, key%256, 
			repr(chr(key%256)) if key%256 < 128 else '?')

	# When everything done, release the capture
	video.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	
	import sys
	
	if len(sys.argv) > 1:
		capture('output/pics/%s.jpg' % sys.argv[1])
	else:
		exit(1)
