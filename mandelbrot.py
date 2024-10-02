import numpy as np
import gc
import cv2
from tqdm import tqdm
from scipy.ndimage import zoom
from moviepy.editor import *
#def zoom_in(array:np.ndarray):
#    array = array[]


def mandelbrot_set(iteration:int, resolution:tuple, videowriter:cv2.VideoWriter):

    def build_grid(xmin, xmax, ymin, ymax)->np.ndarray:
        xline = np.linspace(xmin, xmax,resolution[0])
        yline = np.linspace(ymin, ymax,resolution[1])
        x,y = np.meshgrid(yline,xline)
        return x+1j*y #j: sqrt(-1) image unit
    
    
    z = (0+0j)*np.ones((resolution[0], resolution[1]))
    background = np.zeros((resolution[0], resolution[1], 3))
    lastmask = np.ones((resolution[0], resolution[1], 3))
    
    color = np.array([255,0,0])  

    xmin, xmax, ymin, ymax = -2, 2, -2, 2
    #cx, cy = 0.3001301496, -0.025500022629245
    #cx, cy = 0, 0.02
    
    #zoom_factor_x = 1.08
    #zoom_factor_y = 1.08
    #zoom_cx, zoom_cy = int(zoom_factor_x * 2000 / 2 + zoom_factor_x * 2000 * cx / 4), int( zoom_factor_y * 2500 / 2 + zoom_factor_y * 2500 * cy / 4)
    #zoom_cx, zoom_cy = 1083, 1368
    
    #zoom_factor_x = 1.04
    #zoom_factor_y = 1.04
    #zoom_cx, zoom_cy = 1042, 1309

    #zoom_factor_x = 1.06
    #zoom_factor_y = 1.06
    #zoom_cx, zoom_cy = 1068, 1289
    
    c = build_grid(xmin, xmax, ymin, ymax)

    for i in tqdm(range(iteration)):
        
        
        # discard escaped value
        mask = (abs(z) <= 2).astype(np.int32)
        z = z*mask 
    
        mask = np.repeat(mask[:,:,np.newaxis], 3, axis=2)

        # union along all previous iteration by using the concept of bit-wised AND 
        
        mask = lastmask*mask 
        # Only color for the different pos
        # Please make color smoothly change along with each iteration 
        # Your code for changing color:
        color = np.array([int(256 * np.sin(1 - i / 50)), int(256 * np.cos(i / iteration * 1.5)), int(256 * np.sin(1 - i / 50 * 2))])
        

        framei=(lastmask - mask)*color
       
        background += framei
        lastmask = mask

        # update z : you need to implement this. You can go to check the formula for mandelbrot set
        # Your code:
        z = z**2 + c

        # free mem
        del mask, framei
        gc.collect()

        

        #mask = zoom(mask, [zoom_factor_x, zoom_factor_y], order=1)
        #mask = mask[zoom_cx - 1000 : zoom_cx + 1000, zoom_cy - 1250 : zoom_cy + 1250]
        
        #if i <= 50:
        zoom_factor_x = 1.08
        zoom_factor_y = 1.08
        zoom_cx, zoom_cy = 1088, 1314
        
        
        if i >= 150:
            if i % 3 != 0:
                continue
        """
        elif i >= 120:
            if i % 5 != 0:
                continue
        elif i >= 160:
            if i % 6 != 0:
                continue
        elif i >= 220:
            if i % 2 != 0:
                continue
        """
        

        fram = background.astype(np.uint8)
        videowriter.write(fram)

        z = zoom(z, [zoom_factor_x, zoom_factor_y], order=1, mode='nearest', grid_mode=True)
        z = z[zoom_cx - 1000 : zoom_cx + 1000, zoom_cy - 1250 : zoom_cy + 1250 ]
        lastmask = zoom(lastmask, [zoom_factor_x, zoom_factor_y, 1], order=1, mode='nearest', grid_mode=True)
        lastmask = lastmask[zoom_cx - 1000 : zoom_cx + 1000, zoom_cy - 1250  : zoom_cy + 1250 , :]
        background = zoom(background, [zoom_factor_x, zoom_factor_y, 1], order=1, mode='nearest', grid_mode=True)
        background = background[zoom_cx - 1000 : zoom_cx + 1000, zoom_cy - 1250: zoom_cy + 1250 , :]  
        c = zoom(c, [zoom_factor_x, zoom_factor_y], order=1, mode='nearest', grid_mode=True)
        c = c[zoom_cx - 1000 : zoom_cx + 1000, zoom_cy - 1250 : zoom_cy + 1250 ]


        """
        xmin = cx - (cx - xmin) / zoom_factor_x
        xmax = cx + (xmax - cx) / zoom_factor_x
        ymin = cy - (cy - ymin) / zoom_factor_y
        ymax = cy + (ymax - cy) / zoom_factor_y
        """
        

    
    return

def main():
    resolutionY, resolutionX = (2500, 2000)
    videowriter = cv2.VideoWriter("test10881314b.mp4", cv2.VideoWriter_fourcc('m','p','4','v'), 10.0, (resolutionY, resolutionX))  
    
   
    mandelbrot_set(iteration=20, resolution=(resolutionX,resolutionY), videowriter = videowriter)

    # Write a frame as image for demostration
    # cv2.imwrite("m100.png", itera_100_frame)
       
    """
    video = VideoFileClip("test.mp4")  # 讀取影片
    audio = AudioFileClip("audio.mp3")        # 讀取音樂

    output = video.set_audio(audio)         # 合併影片與聲音
    output.write_videofile("output.mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
    """

if __name__ == "__main__":
   
    main()
