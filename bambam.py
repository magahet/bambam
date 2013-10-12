#!/usr/bin/python
import pygame, sys,os, random, string
from pygame.locals import * 
from subprocess import Popen, PIPE, STDOUT
import re
import pprint

cmd = 'xdpyinfo | grep dim'
p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
output = p.stdout.read()

m = re.search("(\d+)x(\d+)", output)

screen_width = int(m.group(1))
screen_height = int(m.group(2))

print screen_width, screen_height
#sys.exit()

# figure out the install base to use with image and sound loading
progInstallBase = os.path.expanduser("~/Dropbox/gar-jj-noel-micah-share/bambam")


# Load image in data/, handling setting of the transparency color key
def load_image(name, colorkey=None):
    fullname = os.path.join(progInstallBase, 'data', name)
    
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image:", name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

# Load sound file in data/
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join(progInstallBase, 'data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print "Cannot load sound:", fullname
        raise SystemExit, message
    return sound

# Loads a list of sounds
def load_sounds(lst):
    result = []
    for name in lst:
        result.append(load_sound(name))
    return result

# Processes events
def input(events, quit_pos):
    
    try:
        for event in events: 
            if event.type == QUIT: 
                sys.exit(0) 
            elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                #print "eepos: %s" % (quit_pos)
                
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        quit_pos = 1
                    elif ((event.key == K_u) and (quit_pos == 1)):
                        quit_pos = 2
                    elif event.key == K_i and quit_pos == 2:
                        quit_pos = 3
                    elif event.key == K_t and quit_pos == 3:
                        quit_pos = 4
                    else:
                        quit_pos = 0

                # Clear the background 5% of the time
                if random.randint(0, 20) == 1:
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                sound = sounds[random.randint(0, len(sounds) -1)]

                if sound.get_length() > 10:
                    if pygame.mixer.get_busy() == 0:
                        sound.play()
                elif pygame.mixer.get_busy() < 3:
                    sound.play()


                if event.type == MOUSEBUTTONDOWN or not(is_alpha(event.key)):
                    print_image()
                else:
                    print_letter(event.key)
                
                pygame.display.flip() 
        return quit_pos
    except:
        pprint.pprint(locals())

# Prints an image at a random location
def print_image():
    img = images[random.randint(0, len(images) -1)]
    w = random.randint(0, screen_width-img.get_width())
    h = random.randint(0, screen_height-img.get_height())
    screen.blit(img, (w, h)) 

# Is the key that was pressed alphanumeric
def is_alpha(key):
    return key < 255 and (chr(key) in string.letters or chr(key) in string.digits)

# Prints a letter at a random location
def print_letter(key):
    font = pygame.font.Font(None, 256)
    text = font.render(chr(key), 1, colors[random.randint(0, len(colors) -1)])
    textpos = text.get_rect()
    center = (textpos.width / 2, textpos.height / 2)
    w = random.randint(0+center[0], screen_width - center[0])
    h = random.randint(0+center[1], screen_height - center[1])
    textpos.centerx = w
    textpos.centery = h
    screen.blit(text, textpos) 

# Main application
#
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'
 
pygame.init() 
 
window = pygame.display.set_mode((screen_width,screen_height), pygame.FULLSCREEN) 
pygame.display.set_caption('Bam Bam') 
screen = pygame.display.get_surface() 

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

screen.blit(background, (0, 0))
pygame.display.flip()

sounds = load_sounds((elem for elem in os.listdir(os.path.join(progInstallBase, 'data')) if '.ogg' in elem))
colors = ((0,0,255), (255,0,0), (0,255,0), (255, 0, 255),(255, 255, 0))
images = tuple(load_image(elem) for elem in os.listdir(os.path.join(progInstallBase, 'data')) if '.bmp' in elem or '.gif' in elem or '.jpg' in elem)

quit_pos = 0   

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    quit_pos = input(pygame.event.get(), quit_pos) 

    if quit_pos == 4:
        break

